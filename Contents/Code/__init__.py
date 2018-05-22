# Plex IPTV plug-in that plays live streams (like IPTV) from a M3U playlist

# Copyright © 2013-2018 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 2.1.8

from m3u_parser import LoadPlaylist, PlaylistReloader
from xmltv_parser import LoadGuide, GuideReloader
from locale_patch import L, SetAvailableLanguages
import re

NAME = 'IPTV'
PREFIX = '/video/' + NAME.lower()

####################################################################################################
def Start():

    ObjectContainer.title1 = NAME
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    InputDirectoryObject.thumb = R('icon-search.png')
    InputDirectoryObject.art = R('art-default.jpg')
    VideoClipObject.thumb = R('icon-tv.png')
    VideoClipObject.art = R('art-default.jpg')

    SetAvailableLanguages({'en', 'fr', 'ru'})
    
    # in case something went wrong last run (#122)
    Dict['playlist_loading_in_progress'] = False
    Dict['guide_loading_in_progress'] = False

    if Prefs['m3u_reload_time'] == 'on start' or not Dict['groups'] or not Dict['streams']:
        LoadPlaylist()

    Thread.Create(PlaylistReloader)
    Thread.Create(GuideReloader)

####################################################################################################
@handler(PREFIX, NAME)
def MainMenu():

    if Prefs['search'] or Prefs['m3u_manual_reload'] or Prefs['xmltv_manual_reload'] or Prefs['preferences']:
        oc = ObjectContainer()
        oc.add(
            DirectoryObject(
                key = Callback(ListGroups),
                title = unicode(L('View playlist')),
                thumb = R('icon-list.png')
            )
        )
        if Prefs['search']:
            oc.add(
                InputDirectoryObject(
                    key = Callback(ListItems),
                    title = unicode(L('Search')), 
                    #prompt = unicode(L('Search')),
                    thumb = R('icon-search.png')
                )
            )
        if Prefs['m3u_manual_reload']:
            oc.add(
                DirectoryObject(
                    key = Callback(ReloadPlaylist),
                    title = unicode(L('Reload playlist')),
                    thumb = R('icon-reload.png')
                )
            )
        if Prefs['xmltv'] and Prefs['xmltv_manual_reload']:
            oc.add(
                DirectoryObject(
                    key = Callback(ReloadGuide),
                    title = unicode(L('Reload program guide')),
                    thumb = R('icon-reload.png')
                )
            )
        if Prefs['preferences']:
            oc.add(
                PrefsObject(
                    title = unicode(L('Preferences')),
                    thumb = R('icon-prefs.png')
                )
            )
        return oc
    else:
        return ListGroups()

####################################################################################################
@route(PREFIX + '/listgroups', page = int)
def ListGroups(page = 1):

    if not Dict['groups']:
        LoadPlaylist()
        if not Dict['groups']:
            return ObjectContainer(
                        title1 = unicode(L('Error')),
                        header = unicode(L('Error')),
                        message = unicode(L('Provided playlist files are invalid, missing or empty, check the log file for more information'))
                    )

    groups = Dict['groups']
    groups_list = groups.values()

    use_groups = False
    for group in groups_list:
        if group['title'] not in [unicode('All'), unicode('No category')]:
            use_groups = True
            break

    if use_groups:
        if Prefs['sort_groups']:
            # Natural sort (http://stackoverflow.com/a/16090640)
            groups_list.sort(key = lambda d: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', d['title'].lower())])
        else:
            groups_list.sort(key = lambda d: d['order'])
        oc = ObjectContainer(title1 = unicode(L('View playlist')))
        oc.add(
            DirectoryObject(
                key = Callback(ListItems, group = unicode('All')),
                title = unicode(L('All'))
            )
        )
        for group in groups_list:
            if group['title'] not in [unicode('All'), unicode('No category')]:
                thumb = GetImage(group['thumb'], default = 'icon-folder.png', title = group['title'])
                art = GetImage(group['art'], default = 'art-default.png')
                oc.add(
                    DirectoryObject(
                        key = Callback(ListItems, group = group['title']),
                        title = group['title'],
                        thumb = thumb,
                        art = art
                    )
                )
        if unicode('No category') in groups.keys():
            oc.add(
                DirectoryObject(
                    key = Callback(ListItems, group = unicode('No category')),
                    title = unicode(L('No category'))
                )
            )
        return oc
    else:
        return ListItems()

####################################################################################################
@route(PREFIX + '/listitems', page = int)
def ListItems(group = unicode('All'), query = '', page = 1):

    if not Dict['streams']:
        LoadPlaylist()
        if not Dict['streams']:
            return ObjectContainer(
                        title1 = unicode(L('Error')),
                        header = unicode(L('Error')),
                        message = unicode(L('Provided playlist files are invalid, missing or empty, check the log file for more information'))
                    )

    group = unicode(group) # Plex loses unicode formating when passing string between @route procedures if string is not a part of a @route

    streams = Dict['streams']
    items_list = streams.get(group, dict()).values()

    # Filter
    if query:
        raw_items_list = items_list
        ql = query.lower()
        items_list = filter(lambda d: ql in d['title'].lower(), items_list)

        guide = Dict['guide']
        if guide:
            current_datetime = Datetime.Now()
            try:
                guide_hours = int(Prefs['guide_hours'])
            except:
                guide_hours = 8
            crop_time = current_datetime + Datetime.Delta(hours = guide_hours)
            for key in guide.keys():
                # crop anything outside of our window first to limit the second search
                shows = filter(lambda d: d['start'] <= crop_time and d['stop'] > current_datetime, guide[key].values())
                # now look for matches in the result set
                shows = filter(lambda d: ql in d['title'].lower(), shows)
                for show in shows:
                    items_list = items_list + filter(lambda d: show['channel_id'] == d['id'], raw_items_list)

    # Sort
    if Prefs['sort_lists']:
        # Natural sort (http://stackoverflow.com/a/16090640)
        items_list.sort(key = lambda d: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', d['title'].lower())])
    else:
        items_list.sort(key = lambda d: d['order'])

    # Number of items per page
    try:
        items_per_page = int(Prefs['items_per_page'])
    except:
        items_per_page = 40
    items_list_range = items_list[page * items_per_page - items_per_page : page * items_per_page]

    oc = ObjectContainer(title1 = unicode(L('Search')) if query else group)

    for item in items_list_range:
        oc.add(
            CreateVideoClipObject(
                url = item['url'],
                title = item['title'],
                thumb = GetImage(item['thumb'], default = 'icon-tv.png', id = item['id'], name = item['name'], title = item['title']),
                art = GetImage(item['art'], default = 'art-default.jpg'),
                summary = GetSummary(item['id'], item['name'], item['title'], unicode(L('No description available'))),
                c_audio_codec = item['audio_codec'] if item['audio_codec'] else Prefs['audio_codec'] if Prefs['audio_codec'] else None,
                c_video_codec = item['video_codec'] if item['video_codec'] else Prefs['video_codec'] if Prefs['video_codec'] else None,
                c_container = item['container'] if item['container'] else Prefs['container'] if Prefs['container'] else None,
                c_protocol = item['protocol'] if item['protocol'] else Prefs['protocol'] if Prefs['protocol'] else None,
                c_user_agent = item.get('user_agent') if item.get('user_agent') else Prefs['user_agent'] if Prefs['user_agent'] else None,
                optimized_for_streaming = item['optimized_for_streaming'] in ['y', 'yes', 't', 'true', 'on', '1'] if item['optimized_for_streaming'] else Prefs['optimized_for_streaming'],
                include_container = False
            )
        )

    if len(items_list) > page * items_per_page:
        oc.add(
            NextPageObject(
                key = Callback(ListItems, group = group, query = query, page = page + 1),
                thumb = R('icon-next.png')
            )
        )

    if len(oc) > 0:
        return oc
    else:
        return ObjectContainer(
                    title1 = unicode(L('Search')),
                    header = unicode(L('Search')),
                    message = unicode(L('No items were found'))
                )

####################################################################################################
@route(PREFIX + '/createvideoclipobject', include_container = bool)
def CreateVideoClipObject(url, title, thumb, art, summary,
                          c_audio_codec = None, c_video_codec = None,
                          c_container = None, c_protocol = None,
                          c_user_agent = None, optimized_for_streaming = True,
                          include_container = False, *args, **kwargs):

    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject,
                       url = url, title = title, thumb = thumb, art = art, summary = summary,
                       c_audio_codec = c_audio_codec, c_video_codec = c_video_codec,
                       c_container = c_container, c_protocol = c_protocol,
                       c_user_agent = c_user_agent, optimized_for_streaming = optimized_for_streaming,
                       include_container = True),
        rating_key = url,
        title = title,
        thumb = thumb,
        art = art,
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = url, c_user_agent = c_user_agent))
                    )
                ],
                audio_codec = c_audio_codec if c_audio_codec else None,
                video_codec = c_video_codec if c_video_codec else None,
                container = c_container if c_container else None,
                protocol = c_protocol if c_protocol else None,
                optimized_for_streaming = optimized_for_streaming
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco], user_agent = c_user_agent if c_user_agent else None)
    else:
        return vco

####################################################################################################
@indirect
@route(PREFIX + '/playvideo.m3u8')
def PlayVideo(url, c_user_agent = None):

    # Custom User-Agent string
    if c_user_agent:
        HTTP.Headers['User-Agent'] = c_user_agent

    return IndirectResponse(VideoClipObject, key = url)

####################################################################################################
@route(PREFIX + '/reloadplaylist')
def ReloadPlaylist():

    if Dict['playlist_loading_in_progress']:
        return ObjectContainer(
                    title1 = unicode(L('Warning')),
                    header = unicode(L('Warning')),
                    message = unicode(L('Playlist is reloading in the background, please wait'))
                )

    LoadPlaylist()

    if Dict['groups']:
        return ObjectContainer(
                    title1 = unicode(L('Success')),
                    header = unicode(L('Success')),
                    message = unicode(L('Playlist reloaded successfully'))
                )
    else:
        return ObjectContainer(
                    title1 = unicode(L('Error')),
                    header = unicode(L('Error')),
                    message = unicode(L('Provided playlist files are invalid, missing or empty, check the log file for more information'))
                )

####################################################################################################
@route(PREFIX + '/reloadguide')
def ReloadGuide():

    if Dict['guide_loading_in_progress']:
        return ObjectContainer(
                    title1 = unicode(L('Warning')),
                    header = unicode(L('Warning')),
                    message = unicode(L('Program guide is reloading in the background, please wait'))
                )

    LoadGuide()

    if Dict['guide']:
        return ObjectContainer(
                    title1 = unicode(L('Success')),
                    header = unicode(L('Success')),
                    message = unicode(L('Program guide reloaded successfully'))
                )
    else:
        return ObjectContainer(
                    title1 = unicode(L('Error')),
                    header = unicode(L('Error')),
                    message = unicode(L('Provided program guide files are invalid, missing or empty, check the log file for more information'))
                )

####################################################################################################
def GetImage(file_name, default, id = '', name = '', title = ''):

    if Prefs['title_filename'] and not file_name and title:
        file_name = title + '.png'

    if file_name:
        if file_name.startswith('http'):
            return Resource.ContentsOfURLWithFallback(file_name.replace(' ', '%20'), fallback = R(default))
        elif Prefs['images_path']:
            path = Prefs['images_path']
            if path.startswith('http'):
                file_name = path + file_name if path.endswith('/') else path + '/' + file_name
                return Resource.ContentsOfURLWithFallback(file_name.replace(' ', '%20'), fallback = R(default))
            else:
                if '/' in path and not '\\' in path:
                    # must be unix system, might not work
                    file_name = path + file_name if path.endswith('/') else path + '/' + file_name
                elif '\\' in path and not '/' in path:
                    file_name = path + file_name if path.endswith('\\') else path + '\\' + file_name
        r = R(file_name)
        if r:
            return r

    icons = Dict['icons']
    if icons and (id or name or title):
        key = None
        if id:
            if id in icons.keys():
                key = id
        if not key:
            channels = Dict['channels']
            if channels:
                if name:
                    if name in channels.keys():
                        id = channels[name]
                        if id in icons.keys():
                            key = id
                if not key:
                    if title:
                        if title in channels.keys():
                            id = channels[title]
                            if id in icons.keys():
                                key = id
        if key:
            file_name = icons[key]
            if file_name.startswith('http'):
                return Resource.ContentsOfURLWithFallback(file_name.replace(' ', '%20'), fallback = R(default))

    return R(default)

####################################################################################################
def GetSummary(id, name, title, default = ''):

    summary = ''
    guide = Dict['guide']

    if guide:
        key = None
        if id:
            if id in guide.keys():
                key = id
        if not key:
            channels = Dict['channels']
            if channels:
                if name:
                    if name in channels.keys():
                        id = channels[name]
                        if id in guide.keys():
                            key = id
                if not key:
                    if title:
                        if title in channels.keys():
                            id = channels[title]
                            if id in guide.keys():
                                key = id
        if key:
            items_list = guide[key].values()
            if items_list:
                current_datetime = Datetime.Now()
                try:
                    guide_hours = int(Prefs['guide_hours'])
                except:
                    guide_hours = 8
                for item in items_list:
                    if item['start'] <= current_datetime + Datetime.Delta(hours = guide_hours) and item['stop'] > current_datetime:
                        try:
                            guide_offset_seconds = int(Prefs['guide_offset_seconds'])
                        except:
                            guide_offset_seconds = 0

                        try:
                            guide_format_string = Prefs['guide_format_string']
                        except:
                            guide_format_string = '%H:%M'

                        start = (item['start'] + Datetime.Delta(seconds = guide_offset_seconds)).strftime(guide_format_string)
                        if summary:
                            summary = summary + '\n' + start
                        else:
                            summary = start
                        if item['title']:
                            summary = summary + ' ' + item['title']
                            if item['episode']:
                                summary = summary + ' (' + item['episode'] + ')'
                        if item['desc']:
                            summary = summary + ' - ' + item['desc']

    if summary:
        return summary
    else:
        return default

####################################################################################################
def ValidatePrefs():

    pass
