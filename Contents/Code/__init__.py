# Copyright © 2013-2017 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 2.0

from m3u_parser import LoadPlaylist, PlaylistReloader
from xmltv_parser import GuideReloader, GetGuide

TITLE = 'IPTV'
PREFIX = '/video/iptv'

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')

    if not Dict['groups'] or not Dict['streams']:
        LoadPlaylist()
    Thread.Create(PlaylistReloader)
    Thread.Create(GuideReloader)

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

@route(PREFIX + '/groups/{group}', page = int)
def ListItems(group, page = 1):
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
        # Simply adding VideoClipObject usualy does not work because key requires a callback (PlexPlug-inFramework.pdf page 54)
        oc.add(CreateVideoClipObject(
            url = item['url'],
            title = item['title'],
            thumb = item['thumb'],
            art = item['art'],
            summary = summary
        ))
    if len(items_list) > page * items_per_page:
        oc.add(NextPageObject(
            key = Callback(ListItems, group = group, page = page + 1),
            thumb = R('icon-next.png')
        ))
    if len(oc) < 1:
        return ObjectContainer(header = "Empty", message = "There are no more items available") # this should not ever happen
    else:
        return oc

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, art, summary = None, container = False, includeExtras = 0, includeRelated = 0, includeRelatedCount = 0, includeReviews = 0):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, art = art, summary = summary, container = True, includeExtras = includeExtras, includeRelated = includeRelated, includeRelatedCount = includeRelatedCount, includeReviews = includeReviews),
        rating_key = title,
        #url = url, # url attribute invokes URL services check which are not used here
        title = title,
        thumb = GetThumb(thumb, default = 'icon-tv.png'),
        art = GetThumb(art, default = 'art-default.jpg'),
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        # WebKit players and functions WebVideoURL, RTMPVideoURL and WindowsMediaVideoURL are no longer supported by Plex,
                        # HTTPLiveStreamURL sets wrong attributes for non HTTP streams, and redirects are handled by Plex easily when supplying an absolute URL
                        key = url,
                        # iOS client shows permanent loading screen in the foreground if no duration is provided (https://forums.plex.tv/discussion/comment/1293745/#Comment_1293745),
                        # smarter clients understand that it is a live stream and ignore this attribute
                        duration = 86400000 # 24 hours
                    )
                ],
                optimized_for_streaming = Prefs['optimized_for_streaming'] # https://forums.plex.tv/discussion/comment/828497/#Comment_828497
            )
        ]
    )
    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco

@route(PREFIX + '/validateprefs')
def ValidatePrefs():
    return True

def GetThumb(thumb, default = 'icon-tv.png'):
    if thumb and thumb.startswith('http'):
        return thumb
    elif thumb and thumb != '':
        return R(thumb)
    else:
        return R(default)