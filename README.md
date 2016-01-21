## Plex Media Server plugin that plays live streams (a.k.a. IPTV) from a M3U playlist ##
by [Valdas Vaitiekaitis], also known as [Cigaras], version [1.0.11][Changelog]

1. [Introduction][1]
2. [Installation][2]
3. [Playlist structure and examples][3]
4. [Compatible devices and limitations][4]
5. [Supported protocols][5]
6. [Troubleshooting][6]
6. [To do list][7]
7. [Credits and contacts][8]
8. [License][9]

### Introduction ###
Some [ISP] provide their users [IPTV] services, that can be watched over [VLC] on PC or on TV sets, but for TV a [Set-top box] is usually required that is both expensive and inconvenient because of separate remote. [MediaLink], that is pre-installed on most LG TVs, is able to play [IPTV] streams with the help of [Plex Media Server][GetPlex], but it does not has native support for it. One simple solution is to put every single stream url into a separate \*.strm file, load them into Plex library as Home Videos and assign logos and descriptions manually. Or, if You are lucky, You might find a Channel with predefined playlist that suits Your needs or even broadcasts [IPTV] from Your [ISP], but as I was not lucky enough, I decided to take matters into my own hands and created this Channel plugin, that allows to watch network streams from a customisable playlist, thus allowing You to **watch [IPTV] without a [Set-top box]!**

Please read further for instructions on how to [install][2] and [configure][3] this plugin, check [compatible devices][4] and [supported protocols][5], and, if You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### Installation ###
1. Must have [Plex Media Server][GetPlex] installed, obviously;
2. Download the [zip archive](https://github.com/Cigaras/IPTV.bundle/archive/master.zip) and extract it to Plex plugin folder, for more details read the [official channel installation guide](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-):
  * on Windows: *C:\Users\USERNAME\AppData\Local\Plex Media Server\Plug-ins*
  * on Mac: *~Library/Application Support/Plex Media Server/Plug-ins*
  * on Linux: */usr/lib/plexmediaserver/Resources/Plug-ins* or */var/lib/plex/Plex Media Server/Plug-ins*
  * on FreeBSD *usr/pbi/plexmediaserver-amd64/plexdata/Plex\ Media\ Server/Plug-ins/*
3. Rename folder from *IPTV.bundle-master* to *IPTV.bundle*;
3. Edit the playlist, read below for [instructions][3] and [limitations][5];
4. Restart the Plex Media Server;
5. Launch any of [Plex Apps][GetPlex] (that is connected to the server, obviously) and you should see a new category in Your media library called Video Channels or similar, read below for [compatibility and limitations][4].

### Playlist structure and examples ###
Sample playlist is located in *IPTV.bundle\Content\Resources\playlist.m3u*, you can specify other filename in preferences, but You can not change the path to it, only name can be changed.

Online playlist is also supported, You just need to specify a direct link to it, with http part included (like *http://cigaras.tk/test.m3u*). Playlist should be encoded in **[UTF-8](http://en.wikipedia.org/wiki/UTF-8) without [BOM](http://en.wikipedia.org/wiki/Byte_order_mark)**, I recomend using [Notepad++](http://notepad-plus-plus.org/) to check and convert if needed.

Included sample playlist is for testing purposes only, some streams might be dead by now, here is a short list of resources to get started, however please keep in mind, I am not associated with them and not responsible for their content, try it at Your own risk:
  * [FreeTuxTv.net](http://database.freetuxtv.net)
  * [IPTV-Player.com](http://iptv-player.com/?id=database)
  * [HasBahCaIPTV.com](http://hasbahcaiptv.com/index.php?dir=m3u)
  * [IPTV-Tv.blogspot.com](http://iptv-tv.blogspot.com)
  * [TvOnlineStreams.com](http://www.tvonlinestreams.com)
  * [Plex forums](http://forums.plex.tv/discussion/83083/rel-iptv-bundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/p1)
  * [Google.com](http://lmgtfy.com/?q=iptv+m3u)

Playlist supports additional attributes that can be optionally defined inline after #EXTINF:0 and before the name of the media:
  * **group-title** - category name;
  * **tvg-logo**, **logo** - stream logo or icon, can use remote media (url must include http part) or stored images from *\IPTV.bundle\Content\Resources* folder (filename must include extension);
  * **tvg-id** - not used at the moment, will be used for [EPG];
  * **tvg-name** - not used at the moment, will be used for [EPG].

A simple example (see included sample playlist for more):
```
#EXTM3U
#EXTINF:0 tvg-name="Cartoon Network" tvg-id="Cartoon Network" tvg-logo="icon-default.png" group-title="Cartoons",Cartoon Network
http://80.87.146.133:1111/udp/230.3.3.112:5678
#EXTINF:-1 tvg-logo="http://img3.wikia.nocookie.net/__cb20130406103153/logopedia/images/thumb/0/0f/MTV_Logo_2010.svg/200px-MTV_Logo_2010.svg.png" group-title="Music",MTV Dance
http://80.87.146.133:1111/udp/230.3.3.115:5678
```

Read further for more information about [supported protocols and required configurations][5].

### Compatible devices and limitations ###
It is a [known](http://forums.plex.tv/discussion/84637/problems-getting-live-http-stream-into-channel) [fact](https://forums.plexapp.com/index.php/topic/82477-reanimating-kartinatv-plugin-just-started-with-plex/?p=475261) that Plex Media Server does not transcode live streams and leaves this job for clients and streaming sources, so streams **will play only on clients that are able to handle the stream natively**:

* **Desktop Clients**:
  * **[Plex Media Center]** - no longer in production but you can get one from ~~[old Plex Wiki page](https://oldwiki.plexapp.com/index.php?title=Downloads#Plex_Media_Center_.28PMC_-_standalone_client.29)~~  [Plex Downloads Archive][Plex Media Center] or [download.cnet.com](http://download.cnet.com/Plex-Media-Center/3000-2139_4-75754342.html), plays [most streams][5] without problems, latest known version 0.9.5.4;
  * **[Plex Home Theater][GetPlex]** - the [new](http://www.theverge.com/2012/12/24/3801306/plex-desktop-app-rebranded-as-plex-home-theater-adds-airplay-in) Plex Media Center, does not play any streams at all;
  * **[Plex Web]** - most streams do not work, needs [testing][6];
* **Connected Devices**:
  * **Plex for LG TV ([MediaLink])** plays [HTTP and RTSP][5] streams, however MediaLink is not included in most 2013 years TV models so it can be a problem, [Simon J. Hogan](https://forums.plex.tv/index.php/topic/89004-simonjhogans-plex-client-for-lg-smart-tv/) is working on a [Plex client for LG Smart TV](http://simonjhogan.github.io/plex.lg/), however I did not test it;
  * **[PlexConnect](https://forums.plex.tv/index.php?/topic/69410-READ-BEFORE-POSTING) (Apple TV)** - [many](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=496660) [users](https://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/page-4#entry496683) [report](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=538729) [that it](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=545983) does work, You just need to alternate between transcoding options, or [use third party transcoding service](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=539331);
  * **[Plex for Roku][GetPlex]** - for some it [works](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=502904), for some it [does not](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=482524), [wheezycheezel](https://forums.plex.tv/index.php/user/203736-wheezycheezel/) posted [step by step guide](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=544372) for [TVHeadend](https://tvheadend.org/) streams on [Plex forums](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=544372), needs more [testing][6];
  * **[Plex for Chromecast][GetPlex]** - not tested;
  * **[Plex for Google TV][GetPlex]** - not tested;
  * **[Plex for Samsung][GetPlex]** - works, tested by [MACE-Zer0](https://github.com/Cigaras/IPTV.bundle/issues/29);
* **Mobile Devices**:
  * **[Plex for Android][GetPlex]** - usualy does not work, should work with external player like [MX Player](https://play.google.com/store/apps/details?id=com.mxtech.videoplayer.ad), needs [testing][6];
  * **[Plex for iOS][GetPlex]** - [at the moment does not play any streams at all](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=536311);
  * **[Plex for Windows Phone][GetPlex]** - not tested;

Keep in mind that following list is not full because Plex developers are constantly working and updating their software and I do not have the resources to test them all, You can easily test your client by putting stream url into a \*.strm file and loading it into Plex as Home Video as mentioned [above][1] and [below][6], please [contact me][8] if it happens to work on Your device that is listed as not working or unknown.

Also You can try running a dedicated transcoding service and get Your streams in [preferable format](https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?p=539331), [VODServer] is a good and free example.

One more flaw of this plugin is that it has no control over audio tracks if stream has multiple. Some clients can change the track, some can not, but plugin can not predefine one and I have [no solution](http://forums.plexapp.com/index.php/topic/85178-help-request-how-to-change-audio-track-of-a-video/) at the moment.

Read [further][5] for specific configuration required for some streaming protocols.

### Supported protocols ###
1. **[HTTP]** should work on most devices natively, no specific configuration required.

2. **[RTSP]** should work on most devices natively, no specific configuration required.

3. **[RTMP]** requires special Framework Flag that makes plugin incompatible with some older devices/clients (like my TV) and is disabled by default. You can enable it in Preferences, but You need to manually uncomment 14th line in *Info.plist* file for RTMP streams to work: find ```<!--<string>UseRealRTMP</string>-->``` and change it to ```<string>UseRealRTMP</string>```.

    As Plex no longer supports webkit players, You can no longer use full RTMP urls like this:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/ playpath=live_01@13361 swfurl=http://shopnbc.img.entriq.net/img/ShopNBCLivePlayer/main.swf pageurl=http://www.shopnbc.com/
    ```

    You can only use single URL address without attributes, for example:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/live_01@13361
    ```

    If Real RTMP option in preferences is disabled, plugin will try to play stream over HTTP protocol, some streams work that way. If Real RTMP option is enabled, but ```UseRealRTMP``` flag in *Info.plist* file is disabled, then Plex will try to use [its own hosted SWF player](http://www.plexapp.com/player/player.php) and will fail.

4. **[MMS]** did not work for me on any tested devise, but plugin will try to play MMS videos over HTTP protocol.

Keep in mind that all streams are unique and Plex will not be able to play all of them, but not necessary because of plugins fault (read [Compatible devices and limitations][4]). Please try playing stream with [VLC] and using \*.strm file method described [above][4] and [below][6] before blaming this plugin. If \*.strm method works and plugin does not, please [contact me][8].

### Troubleshooting ###
If You encounter errors or some streams do not work please do the following:

1. Make sure the playlist file is [encoded in UTF-8 without BOM][5];

2. Try to play the stream in [VLC] player, if it fails Your stream is invalid and will not play on any device; if it works continue to next step:

3. Create a new file with notepad, write your desired streams url there and save it with \*.strm extension, put it into a folder and load folder into Plex Server as Home Video, try to play it in Plex client, if it fails, Your client is unable to play this stream, try alternative clients; if it works, continue to next step:

4. Check plugin log file *com.plexapp.plugins.iptv.log* located in the folowing folder:
  * on Windows: *C:\Users\USERNAME\AppData\Local\Plex Media Server\Logs\PMS Plugin Logs\*
  * on Mac: *~Library/Application Support/Plex Media Server/Logs/PMS Plugin Logs/*

5. If You do not have a solution after checking the log file, submit a [ticket on GitHub](https://github.com/Cigaras/IPTV.bundle/issues/new) or post on [Plex forum](http://forums.plex.tv/discussion/83083/rel-iptv-bundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/p1) with log and playlist files attached and I will try to help You.

### To do list ###
* [EPG];
* Get rid of the list variable and sort the dictionary;
* Possibility to predefine audio track, if ever becomes possible;
* [MMS] protocol troubleshooting;
* Use Plex Services.

### Credits and contacts ###
* Developer: [Valdas Vaitiekaitis], also known as [Cigaras];
* Contributors: [supergivi](https://github.com/supergivi), [sander1](https://github.com/sander1), [Funtic](https://github.com/Funtic) and many others;
* [Artwork](http://www.flickr.com/photos/purplesherbet/10579021143) by photographer D. Sharon Pruitt, owner of [Purple Sherbet Photography](http://www.flickr.com/photos/purplesherbet/), licensed under [CC Attribution 2.0](http://creativecommons.org/licenses/by/2.0);
* [Icons](http://www.iconarchive.com/show/ultrabuuf-icons-by-mattahan.html) by artist Paul Davey, also known as [Mattahan](http://mattahan.deviantart.com/), licensed under [CC Attribution-Noncommercial-Share Alike 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0);
* Advisors: [shopgirl284](http://forums.plexapp.com/index.php/user/87889-shopgirl284/), [Mikedm139](http://forums.plexapp.com/index.php/user/14450-mikedm139/).

If You have any questions or suggestions, please feel free to contact me via [GitHub](https://github.com/Cigaras) or [Plex forum](http://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/), or, if You are Lithuanian, please visit my personal blog at [www.Cigaras.tk](http://Cigaras.tk). If You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### License ###
Copyright © 2013-2015 Valdas Vaitiekaitis

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

  [1]: #introduction "Introduction"
  [2]: #installation "Installation"
  [3]: #playlist-structure-and-examples "Playlist structure and examples"
  [4]: #compatible-devices-and-limitations "Compatible devices and limitations"
  [5]: #supported-protocols "Supported protocols"
  [6]: #troubleshooting "Troubleshooting"
  [7]: #to-do-list "To do list"
  [8]: #credits-and-contacts "Credits and contacts"
  [9]: #license "License"
  [Changelog]: https://github.com/Cigaras/IPTV.bundle/blob/master/CHANGELOG.md
  [Cigaras]: http://forums.plex.tv/profile/Cigaras
  [Valdas Vaitiekaitis]: https://plus.google.com/+ValdasVaitiekaitis
  [Set-top box]: http://en.wikipedia.org/wiki/Set-top_box
  [IPTV]: http://en.wikipedia.org/wiki/IPTV
  [GetPlex]: https://www.plex.tv/downloads
  [Plex Web]: https://support.plex.tv/hc/en-us/articles/200288666-Opening-Plex-Web-App
  [Plex Media Center]: https://support.plex.tv/hc/en-us/articles/201142378--Deprecated-Plex-Media-Center-Windows-OS-X
  [MediaLink]: http://www.plexapp.com/medialink
  [VODServer]: http://vodserver.sourceforge.net/
  [VLC]: http://www.videolan.org/vlc/index.html
  [ISP]: http://en.wikipedia.org/wiki/Internet_service_provider
  [HTTP]: http://en.wikipedia.org/wiki/HTTP_Live_Streaming
  [RTSP]: http://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol
  [RTMP]: http://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol
  [MMS]: http://en.wikipedia.org/wiki/Microsoft_Media_Server
  [EPG]: http://en.wikipedia.org/wiki/Electronic_program_guide
