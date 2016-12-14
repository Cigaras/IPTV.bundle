# Copyright © 2013-2017 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 1.2.6

from datetime import datetime, timedelta # https://docs.python.org/2/library/datetime.html
import xml.etree.ElementTree # https://docs.python.org/2/library/xml.etree.elementtree.html
import time
import calendar

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

@handler(PREFIX, TITLE)
def MainMenu():
    LoadPlaylist()
    LoadGuide()
    groups_list = GROUPS.values()
    if Prefs['sort_groups']:
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
    if unicode(L('No Category')) in GROUPS.keys():
        oc.add(DirectoryObject(key = Callback(ListItems, group = unicode(L('No Category'))), title = unicode(L('No Category'))))
    oc.add(PrefsObject(title = unicode(L('Preferences')), thumb = R('icon-prefs.png')))
    return oc

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
                    streams_count = streams_count + 1
                    stream = {'url': url, 'title': title, 'id': id, 'name': name, 'thumb': thumb, 'order': streams_count}
                    if not STREAMS:
                        STREAMS.setdefault(unicode(L('All')), {})[streams_count] = stream
                    if STREAMS:
                        if not any(item['url'] == stream['url'] for item in STREAMS[unicode(L('All'))].values()):
                            STREAMS.setdefault(unicode(L('All')), {})[streams_count] = stream
                        group_title = GetAttribute(line, 'group-title', default = unicode(L('No Category')))
                        if group_title not in GROUPS.keys():
                            group_thumb = GetAttribute(line, 'group-logo')
                            groups_count = groups_count + 1
                            group = {'title': group_title, 'thumb': group_thumb, 'order': groups_count}
                            GROUPS[group_title] = group
                        if group_title in STREAMS.keys():
                            if not any(item['url'] == stream['url'] for item in STREAMS[group_title].values()):
                                STREAMS.setdefault(group_title, {})[streams_count] = stream
                        else:
                            STREAMS.setdefault(group_title, {})[streams_count] = stream
                    i = i + 1 # skip the url line for the next cycle
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
            start = datetime_from_utc_to_local(programme.get('start'))
            stop = datetime_from_utc_to_local(programme.get('stop'))
            title = programme.find('title').text
            count = count + 1
            item = {'start': start, 'stop': stop, 'title': title, 'order': count}
            GUIDE.setdefault(channel, {})[count] = item
    return None

@route(PREFIX + '/groups/{group}', page = int)
def ListItems(group, page = 1):
    oc = ObjectContainer(title1 = group)
    items_list = STREAMS[group].values()
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
    if len(items_list) > page * items_per_page:
        oc.add(NextPageObject(key = Callback(ListItems, group = group, page = page + 1), title = L("Next Page ...")))
    if len(oc) < 1:
        return ObjectContainer(header = "Empty", message = "There are no more items available") # this should not ever happen
    else:
        return oc

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

def datetime_from_utc_to_local(input_datetime):
    # Get local offset from UTC in seconds
    local_offset_in_seconds = calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime(time.mktime(time.localtime())))
    # Split time from offset
    input_datetime_split = input_datetime.split(" ")
    input_datetime_only = input_datetime_split[0]
    # Convert input date to a proper date
    input_datetime_only_dt = datetime.strptime(input_datetime_only, '%Y%m%d%H%M%S')
    # If exists - convert input_offset_only to seconds otherwise set to 0
    if len(input_datetime_split) > 1:
        input_offset_only = input_datetime_split[1]
        input_offset_mins, input_offset_hours = int(input_offset_only[3:]), int(input_offset_only[:-2])
        input_offset_in_total_seconds = (input_offset_hours * 60 * 60) + (input_offset_mins * 60);
    else:
        input_offset_in_total_seconds = 0
    # Get the true offset taking into account local offset
    true_offset_in_seconds = local_offset_in_seconds + input_offset_in_total_seconds
    # Add the true_offset to input_datetime
    local_dt = input_datetime_only_dt + timedelta(seconds=true_offset_in_seconds)
    return local_dt

def GetGuide(channel):
    summary = ''
    if channel in GUIDE.keys():
        current_time = datetime.today()
        try:
            guide_hours = int(Prefs['guide_hours'])
        except:
            guide_hours = 8
        items_list = GUIDE[channel].values()
        for item in items_list:
            if item['start'] <= current_time + timedelta(hours = guide_hours) and item['stop'] > current_time:
                summary = summary + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title']
    return summary

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, summary = None, container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, container = True),
        rating_key = title,
        url = url,
        title = title,
        thumb = GetThumb(thumb),
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = GetVideoURL(url = url),
                        # iOS client shows permanent loading screen in the foreground if no duration is provided (https://forums.plex.tv/discussion/comment/1293745/#Comment_1293745),
                        # smarter clients understand that it is a live stream and ignore this property
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

try:
    any
except NameError:
    def any(s):
        for v in s:
            if v:
                return True
        return False
