####################################################################################################
def LoadPlaylist():

    groups = {}
    streams = {}
    m3u_files = Prefs['playlist'].split(';')
    for m3u_file in m3u_files:
        if m3u_file:

            if m3u_file.startswith('http://') or m3u_file.startswith('https://'):
                playlist = HTTP.Request(m3u_file).content
            else:
                playlist = Resource.Load(m3u_file, binary = True)

            if playlist:
                lines = playlist.splitlines()
                groups_count = 0
                streams_count = 0
                for i in range(len(lines) - 1):
                    line = lines[i].strip()
                    if line.startswith('#EXTINF'):
                        url = lines[i + 1].strip()
                        if url.startswith('#EXTVLCOPT') and i + 1 < len(lines):
                            # skip VLC specific run-time options
                            i = i + 1
                            url = lines[i + 1].strip()
                        if url != '' and not url.startswith('#'):
                            title = line[line.rfind(',') + 1:len(line)].strip()
                            id = GetAttribute(line, 'tvg-id')
                            name = GetAttribute(line, 'tvg-name')
                            thumb = GetAttribute(line, 'tvg-logo')
                            if thumb == '':
                                thumb = GetAttribute(line, 'logo')
                            art = GetAttribute(line, 'art')
                            streams_count = streams_count + 1
                            stream = {
                                'url': url,
                                'title': title,
                                'id': id,
                                'name': name,
                                'thumb': thumb,
                                'art': art,
                                'order': streams_count
                            }
                            if not streams:
                                streams.setdefault(unicode(L('All')), {})[streams_count] = stream
                            if streams:
                                if not any(item['url'] == stream['url'] for item in streams[unicode(L('All'))].values()):
                                    streams.setdefault(unicode(L('All')), {})[streams_count] = stream
                                group_title = GetAttribute(line, 'group-title', default = unicode(L('No Category')))
                                if group_title not in groups.keys():
                                    group_thumb = GetAttribute(line, 'group-logo')
                                    group_art = GetAttribute(line, 'group-art')
                                    groups_count = groups_count + 1
                                    group = {
                                        'title': group_title,
                                        'thumb': group_thumb,
                                        'art': group_art,
                                        'order': groups_count
                                    }
                                    groups[group_title] = group
                                if group_title in streams.keys():
                                    if not any(item['url'] == stream['url'] for item in streams[group_title].values()):
                                        streams.setdefault(group_title, {})[streams_count] = stream
                                else:
                                    streams.setdefault(group_title, {})[streams_count] = stream
                            i = i + 1 # skip the url line for the next cycle

    Dict['groups'] = groups
    Dict['streams'] = streams
    Dict['last_playlist_load_prefs'] = Prefs['playlist']
    Dict['last_playlist_load_datetime'] = Datetime.Now()

    return None

####################################################################################################
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

####################################################################################################
def PlaylistReloader():

    while True:
        if Prefs['playlist']:
            if Prefs['playlist'] != Dict['last_playlist_load_prefs'] or not Dict['last_playlist_load_datetime']:
                LoadPlaylist()
            elif Prefs['m3u_reload_time'] != 'never':
                current_datetime = Datetime.Now()
                next_load_datetime = Datetime.ParseDate(str(current_datetime.date()) + ' ' + Prefs['m3u_reload_time'] + ':00')
                if current_datetime > next_load_datetime and next_load_datetime > Dict['last_playlist_load_datetime']:
                    LoadPlaylist()
        Thread.Sleep(60)

####################################################################################################
try:
    any
except NameError:
    def any(s):
        for v in s:
            if v:
                return True
        return False