# Plex IPTV plug-in that plays live streams (like IPTV) from a M3U playlist

# Copyright © 2013-2017 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 2.0.5

from m3u_parser import LoadPlaylist, PlaylistReloader
from xmltv_parser import GuideReloader
import re

NAME = 'IPTV'
PREFIX = '/video/iptv'

####################################################################################################
def Start():

    ObjectContainer.title1 = NAME
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.thumb = R('icon-tv.png')
    VideoClipObject.art = R('art-default.jpg')

    if Prefs['m3u_reload_time'] == 'never' or not Dict['groups'] or not Dict['streams']:
        LoadPlaylist()

    Thread.Create(PlaylistReloader)
    Thread.Create(GuideReloader)

####################################################################################################
@handler(PREFIX, NAME)
def MainMenu():

    if not Dict['groups']:
        LoadPlaylist()
        if not Dict['groups']:
            return ObjectContainer(header = unicode(L("Error")), message = unicode(L("Provided playlist files are invalid, missing or empty, check the log file for more information")))

    groups = Dict['groups']
    groups_list = groups.values()

    use_groups = False
    for group in groups_list:
        if group['title'] not in [unicode(L('All')), unicode(L('No Category'))]:
            use_groups = True
            break

    if use_groups:
        if Prefs['sort_groups']:
            # Natural sort (http://stackoverflow.com/a/16090640)
            groups_list.sort(key = lambda dict: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', dict['title'].lower())])
        else:
            groups_list.sort(key = lambda dict: dict['order'])
        oc = ObjectContainer()
        oc.add(
            DirectoryObject(
                key = Callback(ListItems, group = unicode(L('All'))),
                title = unicode(L('All'))
            )
        )
        for group in groups_list:
            if group['title'] not in [unicode(L('All')), unicode(L('No Category'))]:
                thumb = GetImage(group['thumb'], default = 'icon-folder.png')
                art = GetImage(group['art'], default = 'art-default.png')
                oc.add(
                    DirectoryObject(
                        key = Callback(ListItems, group = group['title']),
                        title = group['title'],
                        thumb = thumb,
                        art = art
                    )
                )
        if unicode(L('No Category')) in groups.keys():
            oc.add(
                DirectoryObject(
                    key = Callback(ListItems, group = unicode(L('No Category'))),
                    title = unicode(L('No Category'))
                )
            )
        return oc
    else:
        return ListItems(unicode(L('All')))

####################################################################################################
@route(PREFIX + '/listitems', page = int)
def ListItems(group, page = 1):

    if not Dict['streams']:
        LoadPlaylist()
        if not Dict['streams']:
            return ObjectContainer(header = unicode(L("Error")), message = unicode(L("Provided playlist files are invalid, missing or empty, check the log file for more information")))

    group = unicode(group) # Plex loses unicode formating when passing string between @route procedures if string is not a part of a @route

    streams = Dict['streams']
    items_list = streams.get(group, dict()).values()

    # Sort
    if Prefs['sort_lists']:
        # Natural sort (http://stackoverflow.com/a/16090640)
        items_list.sort(key = lambda dict: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', dict['title'].lower())])
    else:
        items_list.sort(key = lambda dict: dict['order'])

    # Number of items per page
    try:
        items_per_page = int(Prefs['items_per_page'])
    except:
        items_per_page = 40
    items_list_range = items_list[page * items_per_page - items_per_page : page * items_per_page]

    oc = ObjectContainer(title1 = group)

    for item in items_list_range:
        oc.add(
            CreateVideoClipObject(
                url = item['url'],
                title = item['title'],
                thumb = GetImage(item['thumb'], 'icon-tv.png'),
                art = GetImage(item['art'], 'art-default.jpg'),
                summary = GetSummary(item['id'], item['name'], item['title'], unicode(L("No description available"))),
                c_audio_codec = item['audio_codec'] if item['audio_codec'] else None,
                c_video_codec = item['video_codec'] if item['video_codec'] else None,
                c_container = item['container'] if item['container'] else None,
                c_protocol = item['protocol'] if item['protocol'] else None,
                optimized_for_streaming = item['optimized_for_streaming'] in ['y', 'yes', 't', 'true', 'on', '1'] if item['optimized_for_streaming'] else Prefs['optimized_for_streaming'],
                include_container = False
            )
        )

    if len(items_list) > page * items_per_page:
        oc.add(
            NextPageObject(
                key = Callback(ListItems, group = group, page = page + 1),
                thumb = R('icon-next.png')
            )
        )

    if len(oc) > 0:
        return oc
    else:
        return ObjectContainer(header = "Empty", message = "There are no more items available")

####################################################################################################
@route(PREFIX + '/createvideoclipobject', include_container = bool)
def CreateVideoClipObject(url, title, thumb, art, summary,
                          c_audio_codec = None, c_video_codec = None,
                          c_container = None, c_protocol = None,
                          optimized_for_streaming = True,
                          include_container = False, *args, **kwargs):

    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject,
                       url = url, title = title, thumb = thumb, art = art, summary = summary,
                       c_audio_codec = c_audio_codec, c_video_codec = c_video_codec,
                       c_container = c_container, c_protocol = c_protocol,
                       optimized_for_streaming = optimized_for_streaming,
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
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = url))
                    )
                ],
                audio_codec = c_audio_codec,
                video_codec = c_video_codec,
                container = c_container,
                protocol = c_protocol,
                optimized_for_streaming = optimized_for_streaming
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco])
    else:
        return vco

####################################################################################################
@indirect
@route(PREFIX + '/playvideo.m3u8')
def PlayVideo(url):

    # Custom User-Agent string
    if Prefs['user_agent']:
        HTTP.Headers['User-Agent'] = Prefs['user_agent']

    return IndirectResponse(VideoClipObject, key = url)

####################################################################################################
def GetImage(file_name, default):

    if file_name:
        if file_name.startswith('http'):
            return Resource.ContentsOfURLWithFallback(file_name, fallback = R(default))
        if Prefs['images_path']:
            path = Prefs['images_path']
            if path.startswith('http'):
                file_name = path + file_name if path.endswith('/') else path + '/' + file_name
                return Resource.ContentsOfURLWithFallback(file_name, fallback = R(default))
            else:
                if '/' in path and not '\\' in path:
                    # must be unix system, might not work
                    file_name = path + file_name if path.endswith('/') else path + '/' + file_name
                elif '\\' in path and not '/' in path:
                    file_name = path + file_name if path.endswith('\\') else path + '\\' + file_name
        r = R(file_name)
        if r:
            return r
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
                        if summary:
                            summary = summary + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title']
                        else:
                            summary = item['start'].strftime('%H:%M') + ' ' + item['title']
                        if item['desc']:
                            summary = summary + ' - ' + item['desc']

    if summary:
        return summary
    else:
        return default

####################################################################################################
def ValidatePrefs():

    pass