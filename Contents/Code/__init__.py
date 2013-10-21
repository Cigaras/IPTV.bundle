# Copyright (c) 2013 Valdas Vaitiekaitis, a.k.a. Cigaras. All rights reserved.

PREFIX = '/video/iptv'
TITLE = 'IPTV'

def Start():
    ObjectContainer.title1 = TITLE

    # Default icon for directories (groups)
    DirectoryObject.thumb = R('icon-default.png')

@handler(PREFIX, TITLE)
def MainMenu():
    items_list = []
    groups_list = []
    playlist = Resource.Load('playlist.m3u', binary = True)
    if playlist <> None:
        lines = playlist.splitlines()
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            if line.startswith('#EXTINF'):
                url = lines[i + 1].strip()
                title = line[line.rfind(',') + 1:len(line)].strip()
                thumb = GetParm(line, 'tvg-logo')
                group = GetParm(line, 'group-title')
                items_list.append({'url': url, 'title': title, 'thumb': thumb, 'group': group})
                if group <> '' and not group in groups_list:
                    groups_list.append(group)
        items_list.sort(key = lambda dict: dict['title'].lower())
        groups_list.sort(key = lambda str: str.lower())
        groups_list.insert(0, 'All')
        groups_list.append('Uncategorized')

    if len(items_list) < 1:
        return ObjectContainer(header="No items found", message="Make sure file playlist.m3u is present and not empty in plugins Resources folder")

    oc = ObjectContainer()

    for group in groups_list:
        oc.add(DirectoryObject(
            key = Callback(ItemsMenu, items_list = items_list, group = group),
            title = group
        ))

    return oc

@route(PREFIX + '/itemsmenu', items_list = list)
def ItemsMenu(items_list, group):
    oc = ObjectContainer(title1 = group)
    for item in items_list:
        if item['group'] == group or group == 'All' or (item['group'] == '' and group == 'Uncategorized'):
            url = item['url']
            title = item['title']
            thumb = item['thumb']
            oc.add(VideoClipObject(
                key = Callback(Lookup, url = url, title = title, thumb = thumb),
                rating_key = url,
                title = title,
                thumb = thumb,
                items = [
                    MediaObject(
                        #container = Container.MP4,     # MP4, MKV, MOV, AVI
                        #video_codec = VideoCodec.H264, # H264
                        #audio_codec = AudioCodec.AAC,  # ACC, MP3
                        #audio_channels = 2,            # 2, 6
                        #parts = [PartObject(key = HTTPLiveStreamURL(url))],
                        parts = [PartObject(key = url)],
                        optimized_for_streaming = True
                    )
                ]
            ))
    return oc

@route(PREFIX + '/lookup')
def Lookup(url, title, thumb):
    oc = ObjectContainer()
    oc.add(VideoClipObject(
        key = Callback(Lookup, url = url, title = title, thumb = thumb),
        rating_key = url,
        title = title,
        thumb = thumb,
        items = [
            MediaObject(
                #container = Container.MP4,
                #video_codec = VideoCodec.H264,
                #audio_codec = AudioCodec.AAC,
                #audio_channels = 2,
                #parts = [PartObject(key = HTTPLiveStreamURL(url))],
                parts = [PartObject(key = url)],
                optimized_for_streaming = True
            )
        ]
    ))
    return oc

def GetParm(text, parm):
    x = text.find(parm)
    if x > -1:
        y = text.find('"', x + len(parm)) + 1
        z = text.find('"', y)
        return text[y:z].strip()
    else:
        return ''