# Copyright (c) 2013 Valdas Vaitiekaitis, a.k.a. Cigaras. All rights reserved.

TITLE = 'IPTV'
PREFIX = '/video/iptv'
ICON = 'icon-default.png'
ART = 'art-default.jpg'

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)

@handler(PREFIX, TITLE)
def MainMenu():
    items_list = []
    groups_list = []
    empty_group = False
    playlist = Resource.Load(Prefs['playlist'], binary = True)
    if playlist <> None:
        lines = playlist.splitlines()
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            if line.startswith('#EXTINF'):
                url = lines[i + 1].strip()
                title = line[line.rfind(',') + 1:len(line)].strip()
                thumb = GetAttribute(line, 'tvg-logo')
                group = GetAttribute(line, 'group-title')
                items_list.append({'url': url, 'title': title, 'thumb': thumb, 'group': group})
                if group == '':
                    empty_group = True
                elif not group in groups_list:
                    groups_list.append(group)
        items_list.sort(key = lambda dict: dict['title'].lower())
        groups_list.sort(key = lambda str: str.lower())
        groups_list.insert(0, 'All')
        if empty_group:
            groups_list.append('No Category')

    oc = ObjectContainer()
    for group in groups_list:
        oc.add(DirectoryObject(
            key = Callback(ItemsMenu, items_list = items_list, group = group),
            title = group
        ))
    oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON)))
    return oc

@route(PREFIX + '/itemsmenu', items_list = list)
def ItemsMenu(items_list, group):
    oc = ObjectContainer(title1 = group)
    for item in items_list:
        if item['group'] == group or group == 'All' or (item['group'] == '' and group == 'Uncategorized'):
            oc.add(CreateVideoClipObject(
                url = item['url'],
                title = item['title'],
                thumb = item['thumb']
            ))
    return oc

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, include_container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, include_container = True),
        rating_key = title,
        title = title,
        thumb = thumb,
        items = [
            MediaObject(
                #container = Container.MP4,     # MP4, MKV, MOV, AVI
                #video_codec = VideoCodec.H264, # H264
                #audio_codec = AudioCodec.AAC,  # ACC, MP3
                #audio_channels = 2,            # 2, 6
                parts = [PartObject(key = GetVideoURL(url = url))],
                optimized_for_streaming = True
            )
        ]
    )
    if include_container:
        return ObjectContainer(objects=[vco])
    else:
        return vco

def GetVideoURL(url, live = True):
    if url.startswith('rtmp') and Prefs['rtmp']:
        return RTMPVideoURL(url = url, live = live)
    elif url.startswith('mms') and Prefs['mms']:
        return WindowsMediaVideoURL(url = url)
    else:
        return HTTPLiveStreamURL(url = url)

def GetAttribute(text, attribute):
    x = text.find(attribute)
    if x > -1:
        y = text.find('"', x + len(attribute)) + 1
        z = text.find('"', y)
        return text[y:z].strip()
    else:
        return ''