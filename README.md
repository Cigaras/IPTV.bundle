## Plex Media Server plugin to play network streams (a.k.a. IPTV) from a M3U playlist ##
by **Valdas Vaitiekaitis**, also known as **[Cigaras]**, version Beta3

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Playlist structure](#playlist=structure)
4. [Supported protocols](#supported-protocols)
5. [To do list](#to-do-list)
6. [Contacts](#contacts)
7. [License](#license)

### Introduction ###
My [ISP] provides a [IPTV] service to its users and I can watch it over [VLC] on PC without any problems, but if I want to watch it on my TV, I need a [Set-top box] that is both expensive and inconvenient because of separate remote. [MediaLink], that is supported by my TV, is able to play [IPTV] streams with the help of [Plex Media Server], but it does not have a native support for them. One simple solution is to put every single stream url into a separate \*.strm file, load them into library as Home Videos and assign logos and descriptions by hand, not very convenient. If You are lucky, You might find a Video Channel with predefined playlist that suits Your needs or even broadcasts [IPTV] from Your [ISP], but as my [ISP] is barely known to anyone, but as I was not lucky enough, I decided to take matters into my own hands and created this plugin, that allows to watch network streams from a customisable playlist, thus allowing to **watch any [IPTV] without a [Set-top box]**. Please read further for instructions on how to install and configure this plugin, and if You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### Installation ###
1. Must have [Plex Media Server] installed, obviously;
2. Download the [zip archive](https://github.com/afedchin/xbmc-addon-iptvsimple/archive/master.zip) and extract it to Plex plugin folder:
  * on Windows: *C:\Users\USERNAME\AppData\Local\Plex Media Server\Plug-ins*
  * on Mac: *~Library/Application Support/Plex Media Server/Plug-ins*
3. Edit the playlist, read [below for instructions](#playlist-structure);
5. Launch any of [Plex Apps](http://www.plexapp.com/getplex/) (that is connected to the server, obviously) and you should see a new category in Your media library called Video Channels.

### Playlist structure ###
Sample playlist is located in *IPTV.bundle\Content\Resources\playlist.m3u*, you can specify other filename in preferences. Online playlist is also supported, but you must specify a direct link, so [Dropbox](http://dropbox.com) will not work.
Playlist supports additional attributes that can be optionaly defined inline after #EXTINF:0 and before name of the stream (see included sample playlist as example):
* **group-title** - category name;
* **tvg-logo** - a link to logo, if not specified default icon will be used;
* **tvg-id** - not used at the moment, will be used for [EPG];
* **tvg-name** - not used at the moment, will be used for [EPG].

You can find many public streams at [freetuxtv.net](http://database.freetuxtv.net/), [iptv-player.com](http://iptv-player.com/?id=database) and Google, read further for more information about supported protocols and required configurations.

### Supported protocols ###
1. **[HTTP]** should work on most devices natively, no specific configuration required.

2. **[RTSP]** should work on most devices natively, no specific configuration required.

3. **[RTMP]** requires special Framework Flag that makes plugin incompatible with most devices (like my TV) except [desktop clients](http://www.plexapp.com/desktop/) and is disabled by default. You can enable it in Preferences, but You need to manualy uncomment 14th line in *Info.plist* file for RTMP streams to work: find ```<!--<string>UseRealRTMP</string>-->``` and change it to ```<string>UseRealRTMP</string>```.

    There are two ways of writing RTMP url in the playlist: You can define full address with attributes *playpath*, *swfurl* and *pageurl*, then Plex will use provided SWF player, for example:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/ playpath=live_01@13361 swfurl=http://shopnbc.img.entriq.net/img/ShopNBCLivePlayer/main.swf pageurl=http://www.shopnbc.com/
    ```

    or You can use single URL address without attributes, then Plex will use [its own hosted SWF player](http://www.plexapp.com/player/player.php) (some streams require own player and will not playu this way), for example:

    ```
    rtmp://shopnbc.fmsls.entriq.net:443/live/live_01@13361
    ```

    Note that in first example playpath is a separete attribute, but in second example it is combinet into url. If SWF player for RTMP is disabled in preferences, plugin will try to play stream over HTTP protocol, some streams work that way.

4. **[MMS]** uses [Plex's hosted Silverlight player](http://www.plexapp.com/player/silverlight.php), did not work for me on any tested devise so functionality is disabled by default and plugin will try to play MMS videos over HTTP protocol, You can enable it in Preferences.

Keep in mind that all streams are unique and plugin will not be able to play all of them, but not neccesary because of plugins fault. Please try playing stream with [VLC] and using \*.strm file method before blaming this plugin. If \*.strm method works and plugin does not, please [contact me](#contacts).

### To do list ###
* Possibility to choose audio track if stream has multiple;
* [EPG];
* [MMS] protocol troubleshooting;
* Use Plex Services.

### Contacts ###
If You have any questions or suggestions, please feel free to contact me via [GitHub](https://github.com/Cigaras) or [Plex forum](http://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/), or, if You are Lithuanian, please visit my personal blog at [www.Cigaras.tk](http://Cigaras.tk). If You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### License ###
Copyright 2013 Valdas Vaitiekaitis

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

  [Cigaras]: http://forums.plexapp.com/index.php/user/107872-cigaras
  [Plex Media Server]: http://www.plexapp.com/getplex
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
