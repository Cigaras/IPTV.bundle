# M3U files parser for Plex IPTV plug-in that plays live streams (like IPTV) from a M3U playlist

# Copyright © 2013-2018 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os
import urllib2

####################################################################################################
def LoadPlaylist():

    Dict['playlist_loading_in_progress'] = True

    groups = {}
    streams = {}
    m3u_files = Prefs['playlist'].split(';')

    for m3u_file in m3u_files:
        LoadM3UFile(m3u_file, groups, streams)

    Dict['groups'] = groups
    Dict['streams'] = streams
    Dict['last_playlist_load_datetime'] = Datetime.Now()
    Dict['last_playlist_load_prefs'] = Prefs['playlist']
    Dict['last_playlist_load_filename_groups'] = Prefs['filename_groups']
    Dict['playlist_loading_in_progress'] = False

####################################################################################################
def LoadM3UFile(m3u_file, groups = {}, streams = {}, cust_m3u_name = None):

    if m3u_file:

        m3u_name = None
        if Prefs['filename_groups']:
            if cust_m3u_name:
                m3u_name = cust_m3u_name
            else:
                m3u_base = os.path.basename(DecodeURIComponent(m3u_file))
                m3u_name = os.path.splitext(m3u_base)[0]

        if m3u_file.startswith('http://') or m3u_file.startswith('https://'):
            try:
                playlist = HTTP.Request(m3u_file).content
            except:
                playlist = None
        else:
            playlist = Resource.Load(m3u_file, binary = True)

        if playlist:
            stream_count = len(streams)
            lines = playlist.splitlines()
            line_count = len(lines)
            for i in range(line_count - 1):
                line_1 = lines[i].strip()
                if line_1.startswith('#EXTINF'):
                    title = unicode(line_1[line_1.rfind(',') + 1:len(line_1)].strip(), errors = 'replace')
                    id = GetAttribute(line_1, 'tvg-id')
                    name = GetAttribute(line_1, 'tvg-name')
                    thumb = GetAttribute(line_1, 'tvg-logo')
                    if not thumb:
                        thumb = GetAttribute(line_1, 'logo')
                    art = GetAttribute(line_1, 'art')
                    audio_codec = GetAttribute(line_1, 'audio_codec').lower()
                    video_codec = GetAttribute(line_1, 'video_codec').lower()
                    container = GetAttribute(line_1, 'container').lower()
                    protocol = GetAttribute(line_1, 'protocol').lower()
                    user_agent = GetAttribute(line_1, 'user_agent').lower()
                    optimized_for_streaming = GetAttribute(line_1, 'optimized_for_streaming').lower()
                    group_title = GetAttribute(line_1, 'group-title')
                    url = None
                    for j in range(i + 1, line_count):
                        line_2 = lines[j].strip()
                        if line_2:
                            if line_2.startswith('#EXTGRP:') and not group_title:
                                group_title = GetAttribute(line_2, '#EXTGRP', ':', '')
                            elif line_2.startswith('#EXTVLCOPT:') and not user_agent:
                                user_agent = GetAttribute(line_2, 'http-user-agent', '=', '')
                            elif not line_2.startswith('#'):
                                url = line_2
                                i = j + 1
                                break
                    if url:
                        stream_count = stream_count + 1
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
                            'user_agent': user_agent,
                            'optimized_for_streaming': optimized_for_streaming,
                            'order': stream_count
                        }
                        if not streams:
                            streams.setdefault(unicode('All'), {})[stream_count] = stream
                        if streams:
                            if not any(item['url'] == stream['url'] for item in streams[unicode('All')].values()):
                                streams.setdefault(unicode('All'), {})[stream_count] = stream
                            if not group_title:
                                group_title = unicode('No category' if not m3u_name else m3u_name)
                            if group_title not in groups.keys():
                                group_thumb = GetAttribute(line_1, 'group-logo')
                                group_art = GetAttribute(line_1, 'group-art')
                                group = {
                                    'title': group_title,
                                    'thumb': group_thumb,
                                    'art': group_art,
                                    'order': len(groups) + 1
                                }
                                groups[group_title] = group
                            if group_title in streams.keys():
                                if not any(item['url'] == stream['url'] for item in streams[group_title].values()):
                                    streams.setdefault(group_title, {})[stream_count] = stream
                            else:
                                streams.setdefault(group_title, {})[stream_count] = stream
                elif line_1.startswith('#EXTIMPORT'):
                    group_title = unicode(line_1[line_1.rfind(',') + 1:len(line_1)].strip(), errors = 'replace') if line_1.rfind(',') > -1 else None
                    url = None
                    for j in range(i + 1, line_count):
                        line_2 = lines[j].strip()
                        if line_2:
                            if line_2.startswith('#EXTGRP:') and not group_title:
                                group_title = GetAttribute(line_2, '#EXTGRP', ':', '')
                            elif not line_2.startswith('#'):
                                url = line_2
                                i = j + 1
                                break
                    if url:
                        LoadM3UFile(m3u_file = url, groups = groups, streams = streams, cust_m3u_name = group_title)

####################################################################################################
def DecodeURIComponent(uri):

    while True:
        dec = urllib2.unquote(uri)
        if dec == uri:
            break
        uri = dec
    return uri.decode('utf8')

####################################################################################################
def GetAttribute(text, attribute, delimiter1 = '=', delimiter2 = '"', default = ''):

    x = text.lower().find(attribute.lower() + delimiter1 + delimiter2)
    if x > -1:
        y = x + len(attribute) + len(delimiter1) + len(delimiter2)
        z = text.lower().find(delimiter2.lower(), y) if delimiter2 else len(text)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip(), errors = 'replace')
    else:
        return unicode(default, errors = 'replace')

####################################################################################################
def PlaylistReloader():

    while True:
        if Prefs['playlist']:
            if Dict['last_playlist_load_prefs'] != Prefs['playlist'] or Dict['last_playlist_load_filename_groups'] != Prefs['filename_groups'] or not Dict['last_playlist_load_datetime']:
                LoadPlaylist()
            elif Prefs['m3u_reload_time'] != 'on start' and Prefs['m3u_reload_time'] != 'never':
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