## Plex Media Server plugin to play network streams (a.k.a. IPTV) from a M3U playlist ##
by **Valdas Vaitiekaitis**, also known as **[Cigaras]**, version 0.9 RC1

1. [Introduction][1]
2. [Installation][2]
3. [Playlist structure][3]
4. [Compatible devices and limitations][4]
5. [Supported protocols][5]
6. [To do list][6]
7. [Credits and contacts][7]
8. [License][8]

### Introduction ###
Some [ISP] provide their users with [IPTV] services, free or paid, that can be watched over [VLC] on PC or on TV sets, but for TV a [Set-top box] is usualy required that is both expensive and inconvenient because of separate remote. [MediaLink], that is preinstaled on most LG TVs, is able to play [IPTV] streams with the help of [Plex Media Server], but it does not have native support for them. One simple solution is to put every single stream url into a separate \*.strm file, load them into Plex library as Home Videos and assign logos and descriptions by hand. Or, if You are lucky, You might find a Video Channel with predefined playlist that suits Your needs or even broadcasts [IPTV] from Your [ISP], but as I was not lucky enough, I decided to take matters into my own hands and created this plugin, that allows to watch network streams from a customisable playlist, thus allowing to **watch [IPTV] without a [Set-top box]!**

Please read further for instructions on how to [install][2] and [configure][3] this plugin, check [compatible devices][4] and [supported protocols][5], and, if You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### Installation ###
1. Must have [Plex Media Server][GetPlex] installed, obviously;
2. Download the [zip archive](https://github.com/Cigaras/IPTV.bundle/archive/master.zip) and extract it to Plex plugin folder:
  * on Windows: *C:\Users\USERNAME\AppData\Local\Plex Media Server\Plug-ins*
  * on Mac: *~Library/Application Support/Plex Media Server/Plug-ins*
3. Rename folder from *IPTV.bundle-master* to *IPTV.bundle*;
3. Edit the playlist, read below for [instructions][3] and [limitations][5];
5. Launch any of [Plex Apps][GetPlex] (that is connected to the server, obviously) and you should see a new category in Your media library called Video Channels, read below for [compatibility][4].

### Playlist structure ###
Sample playlist is located in *IPTV.bundle\Content\Resources\playlist.m3u*, you can specify other filename in preferences. Online playlist is also supported, but you must specify a direct link, so [Dropbox](http://dropbox.com) will not work (unless You find a way to link directly to m3u file, if You do, please share).
Playlist supports additional attributes that can be optionally defined inline after #EXTINF:0 and before the name of the media (see included sample playlist for an example):
* **group-title** - category name;
* **tvg-logo** - can use remote media (url must include http part) or stored images from \IPTV.bundle\Content\Resources folder (filename must include extension);
* **tvg-id** - not used at the moment, will be used for [EPG];
* **tvg-name** - not used at the moment, will be used for [EPG].

You can find many public streams at [freetuxtv.net](http://database.freetuxtv.net/), [iptv-player.com](http://iptv-player.com/?id=database) and Google, read further for more information about [supported protocols and required configurations](#supported-protocols).

### Compatible devices and limitations ###
It is a [known fact](http://forums.plexapp.com/index.php/topic/84637-problems-getting-live-http-stream-into-channel/?p=488511) that Plex Media Server does not transcode live streams and leaves this job for clients, so streams **will play only on clients that are able to handle the stream natively**, leaving most Android users out of luck. I am unable to provide a list of such devices because Plex developers are constantly working and updating their software and I do not have the resources to test them all, but You can easily test your client by putting stream url into a \*.strm file and loading it into Plex as Home Video as mentioned [above][1].

One more flaw of this plugin is that it has no control over audio tracks if stream has multiple. Some clients can change the track, some can not, but plugin can not predefine one and I have [no solution](http://forums.plexapp.com/index.php/topic/85178-help-request-how-to-change-audio-track-of-a-video/) at the moment.

Read [further][5] for specific configuration required for some streaming protocols.

### Supported protocols ###
1. **[HTTP]** should work on most devices natively, no specific configuration required.

2. **[RTSP]** should work on most devices natively, no specific configuration required.

3. **[RTMP]** requires special Framework Flag that makes plugin incompatible with some devices (like my TV) and is disabled by default. You can enable it in Preferences, but You need to manualy uncomment 14th line in *Info.plist* file for RTMP streams to work: find ```<!--<string>UseRealRTMP</string>-->``` and change it to ```<string>UseRealRTMP</string>```.

    There are two ways of writing RTMP url in the playlist: You can define full address with attributes *playpath*, *swfurl* and *pageurl*, then Plex will use provided SWF player, for example:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/ playpath=live_01@13361 swfurl=http://shopnbc.img.entriq.net/img/ShopNBCLivePlayer/main.swf pageurl=http://www.shopnbc.com/
    ```

    or You can use single URL address without attributes, then Plex will use [its own hosted SWF player](http://www.plexapp.com/player/player.php) (some streams require own player and will not play this way), for example:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/live_01@13361
    ```

    Note that in first example playpath is a separate attribute, but in second example it is combined into url. If SWF player for RTMP is disabled in preferences, plugin will try to play stream over HTTP protocol, some streams work that way.

4. **[MMS]** uses [Plex's hosted Silverlight player](http://www.plexapp.com/player/silverlight.php), did not work for me on any tested devise so functionality is disabled by default and plugin will try to play MMS videos over HTTP protocol, You can enable it in Preferences.

Keep in mind that all streams are unique and Plex will not be able to play all of them, but not necessary because of plugins fault (read [Compatible devices and limitations][4]). Please try playing stream with [VLC] and using \*.strm file method [described above][4] before blaming this plugin. If \*.strm method works and plugin does not, please [contact me][7].

### To do list ###
* [EPG];
* Possibility to predefine audio track, if ever becomes possible;
* [MMS] protocol troubleshooting;
* Use Plex Services.

### Credits and contacts ###
* Developed by Valdas Vaitiekaitis, also known as [Cigaras], with help of:
  * [shopgirl284](http://forums.plexapp.com/index.php/user/87889-shopgirl284/)
  * [Mikedm139](http://forums.plexapp.com/index.php/user/14450-mikedm139/)
* [Artwork] by photographer D. Sharon Pruitt, owner of [Purple Sherbet Photography](http://www.flickr.com/photos/purplesherbet/), available under [Creative Commons Attribution 2.0 Generic license].
* [Icons] by artist Paul Davey, also known as [Mattahan](http://mattahan.deviantart.com/), available under [Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported license].

If You have any questions or suggestions, please feel free to contact me via [GitHub](https://github.com/Cigaras) or [Plex forum](http://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/), or, if You are Lithuanian, please visit my personal blog at [www.Cigaras.tk](http://Cigaras.tk). If You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### License ###
Copyright 2013 Valdas Vaitiekaitis

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

  [1]: #introduction "Introduction"
  [2]: #installation "Installation"
  [3]: #playlist-structure "Playlist structure"
  [4]: #compatible-devices-and-limitations "Compatible devices and limitations"
  [5]: #supported-protocols "Supported protocols"
  [6]: #to-do-list "To do list"
  [7]: #credits-and-contacts "Credits and contacts"
  [8]: #license "License"
  [Cigaras]: http://forums.plexapp.com/index.php/user/107872-cigaras
  [GetPlex]: http://www.plexapp.com/getplex
  [MediaLink]: http://www.plexapp.com/medialink/files/index.html
  [Set-top box]: http://en.wikipedia.org/wiki/Set-top_box
  [IPTV]: http://en.wikipedia.org/wiki/IPTV
  [VLC]: http://www.videolan.org/vlc/index.html
  [ISP]: http://en.wikipedia.org/wiki/Internet_service_provider
  [HTTP]: http://en.wikipedia.org/wiki/HTTP_Live_Streaming
  [RTSP]: http://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol
  [RTMP]: http://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol
  [MMS]: http://en.wikipedia.org/wiki/Microsoft_Media_Server
  [EPG]: http://en.wikipedia.org/wiki/Electronic_program_guide
  [Artwork](http://www.flickr.com/photos/purplesherbet/10579021143)
  [Icons](http://www.iconarchive.com/show/ultrabuuf-icons-by-mattahan.html)
  [Creative Commons Attribution 2.0 Generic license]: http://creativecommons.org/licenses/by/2.0
  [Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported license]: http://creativecommons.org/licenses/by-nc-sa/3.0