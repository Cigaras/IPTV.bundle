                        video_codec = GetAttribute(line, 'video_codec')
                        container = GetAttribute(line, 'container')
                        protocol = GetAttribute(line, 'protocol')
                        optimized_for_streaming = GetAttribute(line, 'optimized_for_streaming').lower()
                        streams_count = streams_count + 1
                        stream = {
                            'url': url,
                            'title': title,
                            'id': id,
                            'name': name,
                            'thumb': thumb,
                            'art': art,
                            'audio_codec': audio_codec,
                            'video_codec': video_codec,
                            'container': container,
                            'protocol': protocol,
                            'optimized_for_streaming': optimized_for_streaming,
                            'order': streams_count
                        }
                        if not streams:
                            streams.setdefault(unicode(L('All')), {})[streams_count] = stream
                        if streams:
                            if not any(item['url'] == stream['url'] for item in streams[unicode(L('All'))].values()):
                                streams.setdefault(unicode(L('All')), {})[streams_count] = stream
                            group_title = GetAttribute(line, 'group-title', default = unicode(L('No Category') if not m3u_name else m3u_name))
                            if group_title not in groups.keys():
                                group_thumb = GetAttribute(line, 'group-logo')
                                group_art = GetAttribute(line, 'group-art')
                                group = {
                                    'title': group_title,
                                    'thumb': group_thumb,
                                    'art': group_art,
                                    'order': len(groups) + 1
                                }
                                groups[group_title] = group
                            if group_title in streams.keys():
                                if not any(item['url'] == stream['url'] for item in streams[group_title].values()):
                                    streams.setdefault(group_title, {})[streams_count] = stream
                            else:
                                streams.setdefault(group_title, {})[streams_count] = stream
                        i = i + 1 # skip the url line for the next cycle
                elif line.startswith('#EXTIMPORT'):
                    url = lines[i + 1].strip()
                    if url != '' and not url.startswith('#'):
                        title = unicode(line[line.rfind(',') + 1:len(line)].strip()) if line.rfind(',') > -1 else None
                        LoadPlaylistOnce(url, groups, streams, title)
                        i = i + 1 # skip the url line for the next cycle
    return None

####################################################################################################
def DecodeURIComponent(uri):

    while True:
        dec = urllib2.unquote(uri)
        if dec == uri:
            break
        uri = dec
    return uri.decode('utf8')
>>>>>>> beta

####################################################################################################
def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"', default = ''):

    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y) if delimiter2 else len(text)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return unicode(default)

####################################################################################################
def PlaylistReloader():

    while True:
        if Prefs['playlist']:
            if Dict['last_playlist_load_prefs'] != Prefs['playlist'] or Dict['last_playlist_load_filename_groups'] != Prefs['filename_groups'] or not Dict['last_playlist_load_datetime']:
                LoadPlaylist()
            elif Prefs['m3u_reload_time'] != 'never':
                current_datetime = Datetime.Now()
                next_load_datetime = Datetime.ParseDate(str(current_datetime.date()) + ' ' + Prefs['m3u_reload_time'] + ':00')
                if current_datetime > next_load_datetime and next_load_datetime > Dict['last_playlist_load_datetime']:
                    LoadPlaylist()
        Thread.Sleep(10)

####################################################################################################
try:
    any
except NameError:
    def any(s):
        for v in s:
            if v:
                return True
        return False