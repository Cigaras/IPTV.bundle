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
    empty_group = False
    groups_list = []
    items_list = []
    if Prefs['playlist'].startswith('http://'):
        playlist = HTTP.Request(Prefs['playlist']).content
    else:
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
                if group == '':
                    empty_group = True
                    group = 'No Category'
                elif not group in groups_list:
                    groups_list.append(group)
                items_list.append({'url': url, 'title': title, 'thumb': thumb, 'group': group})
        items_list.sort(key = lambda dict: dict['title'].lower())
        groups_list.sort(key = lambda str: str.lower())
        groups_list.insert(0, 'All')
        if empty_group:
            groups_list.append('No Category')

    oc = ObjectContainer()
    for group in groups_list:
        oc.add(DirectoryObject(
            key = Callback(ItemsMenu, items_list = items_list, group = group),
            title = L(group)
        ))
    oc.add(PrefsObject(title = L('Preferences'), thumb = R(ICON)))
    return oc

@route(PREFIX + '/itemsmenu', items_list = list)
def ItemsMenu(items_list, group):
    oc = ObjectContainer(title1 = L(group))
    for item in items_list:
        if item['group'] == group or group == 'All':
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
        return ObjectContainer(objects = [vco])
    else:
        return vco

def GetVideoURL(url, live = True):
    if url.startswith('rtmp') and Prefs['rtmp']:
        Log.Debug('*' * 80)
        Log.Debug('* url_before: %s' % url)
        if url.find(' ') > -1:
            # there is no need to split the url into separate attributes, passing everything as url attribute works fine, this is left here for testing
            playpath = GetAttribute(url, 'playpath', '=', ' ')
            swfurl = GetAttribute(url, 'swfurl', '=', ' ')
            pageurl = GetAttribute(url, 'pageurl', '=', ' ')
            url = url[0:url.find(' ')]
            Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live))
            Log.Debug('*' * 80)
            return RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live)
        else:
            Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, live = live))
            Log.Debug('*' * 80)
            return RTMPVideoURL(url = url, live = live)
    elif url.startswith('mms') and Prefs['mms']:
        return WindowsMediaVideoURL(url = url)
    else:
        return HTTPLiveStreamURL(url = url)

def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"'):
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return text[y:z].strip()
    else:
        return ''