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

# Version 2.0.0 beta

from m3u_parser import LoadPlaylist, PlaylistReloader
from xmltv_parser import GuideReloader
from re import split

NAME = 'IPTV'
PREFIX = '/video/iptv'

####################################################################################################
def Start():

    ObjectContainer.title1 = NAME
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.thumb = R('icon-tv.jpg')
    VideoClipObject.art = R('art-default.jpg')

    LoadPlaylist()
    Thread.Create(PlaylistReloader)
    Thread.Create(GuideReloader)

####################################################################################################
@handler(PREFIX, NAME)
def MainMenu():

    groups = Dict['groups']
    groups_list = groups.values()

    use_groups = False
    for group in groups_list:
        if group['title'] not in [unicode(L('All')), unicode(L('No Category'))]:
            use_groups = True
            break

    if use_groups:
        if Prefs['sort_groups']:
            groups_list.sort(key = lambda dict: dict['title'].lower())
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
@route(PREFIX + '/listitems/{group}', page = int)
def ListItems(group, page = 1):

    streams = Dict['streams']
    items_list = streams[group].values()

    # Sort
    if Prefs['sort_lists']:
        # Natural sort (http://stackoverflow.com/a/16090640)
        items_list.sort(key = lambda dict: [int(t) if t.isdigit() else t.lower() for t in split('(\d+)', dict['title'].lower())])
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

        ls_url = item['url']
        ls_title = item['title']
        lo_thumb = GetImage(item['thumb'], 'icon-tv.png')
        lo_art = GetImage(item['art'], 'art-default.jpg')
        ls_summary = GetSummary(item['id'], item['name'], item['title'], unicode(L("No description available")))
        ls_protocol = item['protocol'] if item['protocol'] else None
        ls_audio_codec = item['audio_codec'] if item['audio_codec'] else None
        ls_video_codec = item['video_codec'] if item['video_codec'] else None
        ls_container = item['container'] if item['container'] else None
        #if item['optimized_for_streaming']:
        #    lb_optimized_for_streaming = item['optimized_for_streaming'] in ['y', 'yes', 't', 'true', 'on', '1']
        #else:
        #    lb_optimized_for_streaming = Prefs['optimized_for_streaming']
        lb_optimized_for_streaming = item['optimized_for_streaming'] in ['y', 'yes', 't', 'true', 'on', '1'] if item['optimized_for_streaming'] else Prefs['optimized_for_streaming']

        oc.add(
            CreateVideoClipObject(
                as_url = item['url'],
                as_title = item['title'],
                ao_thumb = GetImage(item['thumb'], 'icon-tv.png'),
                ao_art = GetImage(item['art'], 'art-default.jpg'),
                as_summary = GetSummary(item['id'], item['name'], item['title'], unicode(L("No description available"))),
                as_audio_codec = item['audio_codec'] if item['audio_codec'] else None,
                as_video_codec = item['video_codec'] if item['video_codec'] else None,
                as_container = item['container'] if item['container'] else None,
                as_protocol = item['protocol'] if item['protocol'] else None,
                ab_optimized_for_streaming = lb_optimized_for_streaming,
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
#def CreateVideoClipObject(url, title, thumb, art, summary, protocol, audio_codec, video_codec, optimized_for_streaming, include_container = False, **kwargs):
def CreateVideoClipObject(
    as_url,
    as_title,
    ao_thumb,
    ao_art,
    as_summary,
    as_audio_codec = None,
    as_video_codec = None,
    as_container = None,
    as_protocol = None,
    ab_optimized_for_streaming = True,
    include_container = False,
    **kwargs):

    vco = VideoClipObject(
        #key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, art = art, summary = summary, optimized_for_streaming = optimized_for_streaming, include_container = True),
        key = Callback(
            CreateVideoClipObject,
            as_url = as_url,
            as_title = as_title,
            ao_thumb = ao_thumb,
            ao_art = ao_art,
            as_summary = as_summary,
            as_audio_codec = as_audio_codec,
            as_video_codec = as_video_codec,
            as_container = as_container,
            as_protocol = as_protocol,
            ab_optimized_for_streaming = ab_optimized_for_streaming,
            include_container = True),
        rating_key = as_url,
        title = as_title,
        thumb = ao_thumb,
        art = ao_art,
        summary = as_summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = as_url))
                    )
                ],
                audio_codec = as_audio_codec,
                video_codec = as_video_codec,
                container = as_container,
                protocol = as_protocol,
                optimized_for_streaming = ab_optimized_for_streaming
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
        HTTP.SetHeader('User-Agent', Prefs['user_agent'])

    return IndirectResponse(VideoClipObject, key = url)

####################################################################################################
def GetImage(file_name, default):

    if file_name:
        if file_name.startswith('http'):
            return Resource.ContentsOfURLWithFallback(file_name, fallback = R(default))
        else:
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