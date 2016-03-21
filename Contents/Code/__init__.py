# Copyright © 2013-2016 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 1.1.0

from datetime import datetime, timedelta
import xml.etree.ElementTree

TITLE = 'IPTV'
PREFIX = '/video/iptv'
IPTVMENU = {'All':{}}

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')

def LoadPlaylist():
    global IPTVMENU
    IPTVMENU = {'All':{}}
    if Prefs['playlist'].startswith('http://') or Prefs['playlist'].startswith('https://'):
        playlist = HTTP.Request(Prefs['playlist']).content
    else:
        playlist = Resource.Load(Prefs['playlist'], binary = True)
    if playlist <> None:
        lines = playlist.splitlines()
        count = 0
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            if line.startswith('#EXTINF'):
                url = lines[i + 1].strip()
                title = line[line.rfind(',') + 1:len(line)].strip()
                id = GetAttribute(line, 'tvg-id')
                name = GetAttribute(line, 'tvg-name')
                thumb = GetAttribute(line, 'tvg-logo')
                if thumb == '':
                    thumb = GetAttribute(line, 'logo')
                group = GetAttribute(line, 'group-title', default = unicode(L('No Category')))
                count = count + 1
                item = {'url': url, 'title': title, 'id': id, 'name': name, 'thumb': thumb, 'group': group, 'order': count}
                IPTVMENU.setdefault(unicode(L('All')), {})[count] = item
                IPTVMENU.setdefault(group, {})[count] = item
                i = i + 1 # skip the url line fot next cycle
    return None

@handler(PREFIX, TITLE)
def MainMenu():
    LoadPlaylist()
    groups_list = IPTVMENU.keys()
    if Prefs['sort_groups']:
        groups_list.sort(key = lambda s: s.lower())
    oc = ObjectContainer()
    for group in groups_list:
        oc.add(DirectoryObject(
            key = Callback(ListItems, group = group),
            title = group
        ))
    oc.add(PrefsObject(title = L('Preferences'), thumb = R('icon-prefs.png')))
    return oc

@route(PREFIX + '/groups/{group}')
def ListItems(group):
    oc = ObjectContainer(title1 = group)
    items_list = IPTVMENU[group].values()
    if Prefs['sort_lists']:
        items_list.sort(key = lambda dict: dict['title'].lower())
    else:
        items_list.sort(key = lambda dict: dict['order'])
    for item in items_list:
        #oc.add(VideoClipObject(
        #    url = item['url'],
        #    title = item['title'],
        #    thumb = GetThumb(item['thumb']),
        #    items = [
        #        MediaObject(
        #            parts = [
        #                PartObject(
        #                    key = GetVideoURL(url = item['url']),
        #                )
        #            ],
        #            optimized_for_streaming = True
        #        )
        #    ]
        #))
        if item['id'] != '':
            summary = GetGuide(channel = item['id'])
        if summary == '' and item['name'] != '':
            summary = GetGuide(channel = item['name'])
        if summary == '' and item['title'] != '':
            summary = GetGuide(channel = item['title'])
        # Simply adding VideoClipObject does not work on some clients (like LG SmartTV),
        # so there is an endless recursion - function CreateVideoClipObject calling itself -
        # and I have no idea why and how it works...
        oc.add(CreateVideoClipObject(
            url = item['url'],
            title = item['title'],
            thumb = item['thumb'],
            summary = summary
        ))
    return oc

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, summary, container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, container = True),
        #rating_key = url,
        url = url,
        title = title,
        thumb = GetThumb(thumb),
        summary = summary,
        items = [
            MediaObject(
                #container = Container.MP4,     # MP4, MKV, MOV, AVI
                #video_codec = VideoCodec.H264, # H264
                #audio_codec = AudioCodec.AAC,  # ACC, MP3
                #audio_channels = 2,            # 2, 6
                parts = [
                    PartObject(
                        key = GetVideoURL(url = url)
                    )
                ],
                optimized_for_streaming = True
            )
        ]
    )
    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco

def GetVideoURL(url, live = True):
    if url.startswith('rtmp') and Prefs['rtmp']:
        #Log.Debug('*' * 80)
        #Log.Debug('* url before processing: %s' % url)
        #if url.find(' ') > -1:
        #    playpath = GetAttribute(url, 'playpath', '=', ' ')
        #    swfurl = GetAttribute(url, 'swfurl', '=', ' ')
        #    pageurl = GetAttribute(url, 'pageurl', '=', ' ')
        #    url = url[0:url.find(' ')]
        #    Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live))
        #    Log.Debug('*' * 80)
        #    return RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live)
        #else:
        #    Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, live = live))
        #    Log.Debug('*' * 80)
        #    return RTMPVideoURL(url = url, live = live)
        #Log.Debug('* url after processing: %s' % RTMPVideoURL(url = url, live = live))
        #Log.Debug('*' * 80)
        return RTMPVideoURL(url = url, live = live)
    #elif url.startswith('mms') and Prefs['mms']:
    #    return WindowsMediaVideoURL(url = url)
    else:
        return HTTPLiveStreamURL(url = url)

def GetThumb(thumb):
    if thumb and thumb.startswith('http'):
        return thumb
    elif thumb and thumb <> '':
        return R(thumb)
    else:
        return R('icon-default.png')

def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"', default = ''):
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return default

@route(PREFIX + '/getguide')
def GetGuide(channel):
    # https://docs.python.org/2/library/datetime.html
    # https://docs.python.org/2/library/xml.etree.elementtree.html
    current_time = datetime.today()
    guide = ''
    if Prefs['xmltv'].startswith('http://') or Prefs['xmltv'].startswith('https://'):
        xmltv = HTTP.Request(Prefs['xmltv']).content
    else:
        xmltv = Resource.Load(Prefs['xmltv'], binary = True)
    if xmltv != '':
        root = xml.etree.ElementTree.fromstring(xmltv)
        try:
            guide_hours = int(Prefs['guide_hours'])
        except:
            guide_hours = 8
        for programme in root.findall("./programme[@channel='" + channel + "']"):
            start_time = datetime.strptime(programme.get('start')[:12], '%Y%m%d%H%M')
            stop_time = datetime.strptime(programme.get('stop')[:12], '%Y%m%d%H%M')
            if start_time <= current_time + timedelta(hours = guide_hours) and stop_time > current_time:
                guide = guide + '\n' + start_time.strftime('%H:%M') + ' ' + programme.find('title').text
    return guide
