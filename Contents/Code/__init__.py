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
from xmltv_parser import GuideReloader, GetGuide

TITLE = 'IPTV'
PREFIX = '/video/iptv'

###########################################################################################################################################
def Start():

    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.thumb = R('icon-tv.jpg')
    VideoClipObject.art = R('art-default.jpg')

    LoadPlaylist()
    Thread.Create(PlaylistReloader)
    Thread.Create(GuideReloader)

###########################################################################################################################################
@handler(PREFIX, TITLE)
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
        oc.add(DirectoryObject(key = Callback(ListItems, group = unicode(L('All'))), title = unicode(L('All'))))
        for group in groups_list:
            if group['title'] not in [unicode(L('All')), unicode(L('No Category'))]:
                thumb = GetThumb(group['thumb'], default = 'icon-folder.png')
                art = GetThumb(group['art'], default = 'art-default.png')
                oc.add(DirectoryObject(
                    key = Callback(ListItems, group = group['title']),
                    title = group['title'],
                    thumb = thumb,
                    art = art
                ))
        if unicode(L('No Category')) in groups.keys():
            oc.add(DirectoryObject(key = Callback(ListItems, group = unicode(L('No Category'))), title = unicode(L('No Category'))))
        return oc
    else:
        return ListItems(unicode(L('All')))

###########################################################################################################################################
@route(PREFIX + '/groups/{group}', page = int)
def ListItems(group, page = 1):

    try:
        user_agent = Prefs['user_agent']
    except:
        user_agent = None
    if user_agent:
        oc = ObjectContainer(title1 = group, user_agent = user_agent)
    else:
        oc = ObjectContainer(title1 = group)

    streams = Dict['streams']
    items_list = streams[group].values()

    try:
        items_per_page = int(Prefs['items_per_page'])
    except:
        items_per_page = 40
    if Prefs['sort_lists']:
        items_list.sort(key = lambda dict: dict['title'].lower())
    else:
        items_list.sort(key = lambda dict: dict['order'])

    for item in items_list[page * items_per_page - items_per_page : page * items_per_page]:

        # Get the program guide for the channel
        if item['id'] != '':
            summary = GetGuide(channel = item['id'])
        else:
            summary = ''
        if summary == '' and item['name'] != '':
            summary = GetGuide(channel = item['name'])
        if summary == '' and item['title'] != '':
            summary = GetGuide(channel = item['title'])
        # Some clients fail if summary is left empty
        if not summary:
            summary = item['title']

        oc.add(
            CreateVideoClipObject(
                url = item['url'],
                title = item['title'],
                thumb = item['thumb'],
                art = item['art'],
                summary = summary
            )
        )

    if len(items_list) > page * items_per_page:
        oc.add(NextPageObject(
            key = Callback(ListItems, group = group, page = page + 1),
            thumb = R('icon-next.png')
        ))

    if len(oc) < 1:
        return ObjectContainer(header = "Empty", message = "There are no more items available") # this should not ever happen
    else:
        return oc

###########################################################################################################################################
@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, art, summary = None, include_container = False, **kwargs):

    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, art = art, summary = summary, include_container = True),
        rating_key = title,
        title = title,
        thumb = GetThumb(thumb, default = 'icon-tv.png'),
        art = GetThumb(art, default = 'art-default.jpg'),
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = Callback(PlayVideo, url = url)
                    )
                ],
                optimized_for_streaming = Prefs['optimized_for_streaming']
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco])
    else:
        return vco

###########################################################################################################################################
@route(PREFIX + '/playvideo')
@indirect
def PlayVideo(url):

    # WebKit players and functions WebVideoURL, RTMPVideoURL and WindowsMediaVideoURL are no longer supported by Plex,
    # HTTPLiveStreamURL sets wrong attributes for non HTTP streams,
    # and redirects are handled by Plex easily when supplying an absolute URL
	return IndirectResponse(VideoClipObject, key = url)

###########################################################################################################################################
def GetThumb(thumb, default = 'icon-tv.png'):

    if thumb:
        if thumb.startswith('http'):
            return Resource.ContentsOfURLWithFallback(thumb, fallback = R(default))
        else:
            r = R(thumb)
            if r:
                return r
    return R(default)