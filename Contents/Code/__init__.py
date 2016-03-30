# Copyright © 2013-2016 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 1.2.2

from datetime import datetime, timedelta # https://docs.python.org/2/library/datetime.html
import xml.etree.ElementTree # https://docs.python.org/2/library/xml.etree.elementtree.html

TITLE = 'IPTV'
PREFIX = '/video/iptv'
GROUPS = {}
STREAMS = {}
GUIDE = {}

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')

def LoadPlaylist():
    if Prefs['playlist'].startswith('http://') or Prefs['playlist'].startswith('https://'):
        playlist = HTTP.Request(Prefs['playlist']).content
    else:
        playlist = Resource.Load(Prefs['playlist'], binary = True)
    if playlist != None:
        lines = playlist.splitlines()
        groups_count = 0
        streams_count = 0
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            if line.startswith('#EXTINF'):
                url = lines[i + 1].strip()
                if url != '' and not url.startswith('#'):
                    title = line[line.rfind(',') + 1:len(line)].strip()
                    id = GetAttribute(line, 'tvg-id')
                    name = GetAttribute(line, 'tvg-name')
                    thumb = GetAttribute(line, 'tvg-logo')
                    if thumb == '':
                        thumb = GetAttribute(line, 'logo')
                    group_title = GetAttribute(line, 'group-title', default = unicode(L('No Category')))
                    if group_title not in GROUPS.keys():
                        group_thumb = GetAttribute(line, 'group-logo')
                        groups_count = groups_count + 1
                        group = {'title': group_title, 'thumb': group_thumb, 'order': groups_count}
                        GROUPS[group_title] = group
                    streams_count = streams_count + 1
                    stream = {'url': url, 'title': title, 'id': id, 'name': name, 'thumb': thumb, 'group': group_title, 'order': streams_count}
                    STREAMS.setdefault(unicode(L('All')), {})[streams_count] = stream
                    STREAMS.setdefault(group_title, {})[streams_count] = stream
                    i = i + 1 # skip the url line fot next cycle
    return None

def LoadGuide():
    if Prefs['xmltv'].startswith('http://') or Prefs['xmltv'].startswith('https://'):
        xmltv = HTTP.Request(Prefs['xmltv']).content
    else:
        xmltv = Resource.Load(Prefs['xmltv'], binary = True)
    if xmltv != None:
        root = xml.etree.ElementTree.fromstring(xmltv)
        count = 0
        for programme in root.findall("./programme"):
            channel = programme.get('channel')
            start = datetime.strptime(programme.get('start')[:12], '%Y%m%d%H%M')
            stop = datetime.strptime(programme.get('stop')[:12], '%Y%m%d%H%M')
            title = programme.find('title').text
            count = count + 1
            item = {'start': start, 'stop': stop, 'title': title, 'order': count}
            GUIDE.setdefault(channel, {})[count] = item
    return None

@handler(PREFIX, TITLE)
def MainMenu():
    LoadPlaylist()
    LoadGuide()
    #groups_list = STREAMS.keys()
    groups_list = GROUPS.values()
    if Prefs['sort_groups']:
        #groups_list.sort(key = lambda s: s.lower())
        groups_list.sort(key = lambda dict: dict['title'].lower())
    else:
        groups_list.sort(key = lambda dict: dict['order'])
    oc = ObjectContainer()
    oc.add(DirectoryObject(key = Callback(ListItems, group = unicode(L('All'))), title = unicode(L('All'))))
    for group in groups_list:
        if group['title'] not in [unicode(L('All')), unicode(L('No Category'))]:
            thumb = GetThumb(group['thumb'], default = 'icon-folder.png')
            oc.add(DirectoryObject(
                key = Callback(ListItems, group = group['title']),
                title = group['title'],
                thumb = thumb
            ))
    oc.add(DirectoryObject(key = Callback(ListItems, group = unicode(L('No Category'))), title = unicode(L('No Category'))))
    oc.add(PrefsObject(title = unicode(L('Preferences')), thumb = R('icon-prefs.png')))
    return oc

@route(PREFIX + '/groups/{group}')
def ListItems(group):
    oc = ObjectContainer(title1 = group)
    items_list = STREAMS[group].values()
    if Prefs['sort_lists']:
        items_list.sort(key = lambda dict: dict['title'].lower())
    else:
        items_list.sort(key = lambda dict: dict['order'])
    for item in items_list:
        if item['id'] != '':
            summary = GetGuide(channel = item['id'])
        else:
            summary = ''
        if summary == '' and item['name'] != '':
            summary = GetGuide(channel = item['name'])
        if summary == '' and item['title'] != '':
            summary = GetGuide(channel = item['title'])
        #oc.add(VideoClipObject(
        #    url = item['url'],
        #    title = item['title'],
        #    thumb = GetThumb(item['thumb']),
        #    summary = summary,
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
        rating_key = title,
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

def GetThumb(thumb, default = 'icon-default.png'):
    if thumb and thumb.startswith('http'):
        return thumb
    elif thumb and thumb != '':
        return R(thumb)
    else:
        return R(default)

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

def GetGuide(channel):
    summary = ''
    #if Prefs['xmltv'].startswith('http://') or Prefs['xmltv'].startswith('https://'):
    #    xmltv = HTTP.Request(Prefs['xmltv']).content
    #else:
    #    xmltv = Resource.Load(Prefs['xmltv'], binary = True)
    #if xmltv != '':
    if channel in GUIDE.keys():
        current_time = datetime.today()
        try:
            guide_hours = int(Prefs['guide_hours'])
        except:
            guide_hours = 8
        #root = xml.etree.ElementTree.fromstring(xmltv)
        #for programme in root.findall("./programme[@channel='" + channel + "']"):
        #    start_time = datetime.strptime(programme.get('start')[:12], '%Y%m%d%H%M')
        #    stop_time = datetime.strptime(programme.get('stop')[:12], '%Y%m%d%H%M')
        #    if start_time <= current_time + timedelta(hours = guide_hours) and stop_time > current_time:
        #        summary = summary + '\n' + start_time.strftime('%H:%M') + ' ' + programme.find('title').text
        items_list = GUIDE[channel].values()
        for item in items_list:
            if item['start'] <= current_time + timedelta(hours = guide_hours) and item['stop'] > current_time:
                summary = summary + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title']
    return summary
