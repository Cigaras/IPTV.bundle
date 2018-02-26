# XMLTV files parser for Plex IPTV plug-in that plays live streams (like IPTV) from a M3U playlist

# Copyright © 2013-2018 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import urllib2
import io
import gzip
import xml.etree.ElementTree # Plex XML API fails with big files

####################################################################################################
def LoadGuide():

    Dict['guide_loading_in_progress'] = True

    channels = {}
    icons = {}
    guide = {}
    xmltv_files = Prefs['xmltv'].split(';')

    for xmltv_file in xmltv_files:
        if xmltv_file:
            if xmltv_file.startswith('http://') or xmltv_file.startswith('https://'):
                # Plex can't handle compressed files, using standard Python methods instead
                if xmltv_file.endswith('.gz') or xmltv_file.endswith('.gz?raw=1'):
                    f = io.BytesIO(urllib2.urlopen(xmltv_file).read())
                    try:
                        g = gzip.GzipFile(fileobj = f)
                        xmltv = g.read()
                    except:
                        Log.Error('Provided file %s is not a valid GZIP file' % xmltv_file)
                        xmltv = None
                else:
                    xmltv = HTTP.Request(xmltv_file).content
            else:
                # Local compressed files are not supported at the moment
                xmltv = Resource.Load(xmltv_file, binary = True)

            if xmltv:
                try:
                    #root = XML.ElementFromString(xmltv, encoding = None)
                    root = xml.etree.ElementTree.fromstring(xmltv)
                except:
                    Log.Error('Provided file %s is not a valid XML file' % xmltv_file)
                    root = None
                if root:
                    for channel_elem in root.findall('./channel'):
                        id = channel_elem.get('id')
                        if id:
                            for name in channel_elem.findall('display-name'):
                                try:
                                    key = unicode(name.text, errors = 'replace')
                                except TypeError:
                                    key = name.text.decode('utf-8')
                                if key:
                                    channels[key] = id
                            icon_elem = channel_elem.find('icon')
                            if icon_elem != None: # if icon_elem: does not work
                                src_attr = icon_elem.get('src')
                                if src_attr:
                                    icons[key] = src_attr
                    count = 0
                    current_datetime = Datetime.Now()
                    for programme_elem in root.findall('./programme'):
                        channel_attr = programme_elem.get('channel')
                        try:
                            channel = unicode(channel_attr, errors = 'replace')
                        except TypeError:
                            channel = channel_attr.decode('utf-8')
                        start = StringToLocalDatetime(programme_elem.get('start'))
                        stop = StringToLocalDatetime(programme_elem.get('stop'))
                        if stop >= current_datetime:
                            title_text = programme_elem.findtext("title", default="")
                            try:
                                title = unicode(title_text, errors = 'replace')
                            except TypeError:
                                title = title_text.decode('utf-8')

                            desc_text = programme_elem.findtext("desc", default="")
                            try:
                                desc = unicode(desc_text, errors = 'replace')
                            except TypeError:
                                desc = desc_text.decode('utf-8')

                            ep = programme_elem.find('episode-num')
                            if ep != None:
                                if ep.get('system') == 'xmltv_ns':
                                    fields = ep.text.split('.')
                                    episode_text = "%s%s%s" % (
                                        'S' + fields[0] if len(fields) >= 1 and len(fields[0]) > 0 else '',
                                        'E' + fields[1] if len(fields) >= 2 and len(fields[1]) > 0 else '',
                                        'P' + fields[2] if len(fields) >= 3 and len(fields[2]) > 0 else '')
                                else:
                                    episode_text = ep.text

                                try:
                                    episode = unicode(episode_text, errors = 'replace')
                                except TypeError:
                                    episode = episode_text.decode('utf-8')
                            else:
                                episode = None

                            count = count + 1
                            item = {
                                'start': start,
                                'stop': stop,
                                'title': title,
                                'desc': desc,
                                'episode': episode,
                                'channel_id': channel,
                                'order': count
                            }
                            guide.setdefault(channel, {})[count] = item

    Dict['channels'] = channels
    Dict['icons'] = icons
    Dict['guide'] = guide
    Dict['last_guide_load_datetime'] = Datetime.Now()
    Dict['last_guide_load_prefs'] = Prefs['xmltv']
    Dict['guide_loading_in_progress'] = False

####################################################################################################
def StringToLocalDatetime(arg_string):

    arg_string_split = arg_string.split(' ')
    arg_datetime = Datetime.ParseDate(arg_string_split[0])
    if len(arg_string_split) > 1:
        arg_offset_str = arg_string_split[1]
        arg_offset_hours = int(arg_offset_str[0:3])
        arg_offset_minutes = int(arg_offset_str[3:5])
        arg_offset_seconds = (arg_offset_hours * 60 * 60) + (arg_offset_minutes * 60)
        utc_datetime = arg_datetime - Datetime.Delta(seconds = arg_offset_seconds)
    else:
        utc_datetime = arg_datetime
    loc_offset_seconds = (Datetime.Now() - Datetime.UTCNow()).total_seconds()
    loc_datetime = utc_datetime + Datetime.Delta(seconds = loc_offset_seconds)
    return loc_datetime

####################################################################################################
def GuideReloader():

    while True:
        if Prefs['xmltv']:
            if Prefs['xmltv'] != Dict['last_guide_load_prefs'] or not Dict['last_guide_load_datetime']:
                LoadGuide()
            elif Prefs['xmltv_reload_time'] != 'on start' and Prefs['xmltv_reload_time'] != 'never':
                current_datetime = Datetime.Now()
                next_load_datetime = Datetime.ParseDate(str(current_datetime.date()) + ' ' + Prefs['xmltv_reload_time'] + ':00')
                if current_datetime > next_load_datetime and next_load_datetime > Dict['last_guide_load_datetime']:
                    LoadGuide()
        Thread.Sleep(10)
