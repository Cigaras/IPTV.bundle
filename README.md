## Plex Media Server plugin that plays live streams (a.k.a. IPTV) from a M3U playlist ##
by [Valdas Vaitiekaitis], also known as [Cigaras], version [1.2][Changelog]

1. [Introduction][1]
2. [Installation][2]
3. [Playlist structure and examples][3]
4. [Program guide][4]
4. [Compatible devices and limitations][5]
5. [Supported protocols][6]
6. [Troubleshooting][7]
7. [To do list][8]
8. [Credits and contacts][9]
10. [License][10]

### Introduction ###
Some [ISP] provide their users [IPTV] services, that can be watched over [VLC] on PC or on TV sets, but for TV a [Set-top box] is usually required that is both expensive and inconvenient because of separate remote. [MediaLink], that is pre-installed on most LG TVs, is able to play [IPTV] streams with the help of [Plex Media Server][GetPlex], but it does not has native support for it. One simple solution is to put every single stream url into a separate \*.strm file, load them into Plex library as Home Videos and assign logos and descriptions manually. Or, if You are lucky, You might find a Channel with predefined playlist that suits Your needs or even broadcasts [IPTV] from Your [ISP], but as I was not lucky enough, I decided to take matters into my own hands and created this Channel plugin, that allows to watch network streams from a customisable playlist, thus allowing You to **watch [IPTV] without a [Set-top box]!**

Please read further for instructions on how to [install][2] and [configure][3] this plugin, check [compatible devices][5] and [supported protocols][6], and, if You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### Installation ###
Please refer to ofificial Plex support page [How do I manually install a channel?](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-)

### Playlist structure and examples ###
Sample playlist is located in *IPTV.bundle\Content\Resources\playlist.m3u*, you can specify other filename in preferences, but You can not specifify a path outside resources forder because Plex prohibits it. Online playlist is also supported, You just need to specify a direct link to it, with http part included. Playlist should be encoded in **[UTF-8](http://en.wikipedia.org/wiki/UTF-8) without [BOM](http://en.wikipedia.org/wiki/Byte_order_mark)**, I recomend using [Notepad++](http://notepad-plus-plus.org/) to check and convert if needed.

Included sample playlist is for testing purposes only, some streams might be dead by now, here is a short list of resources to get started, however please keep in mind, I am not associated with them and not responsible for their content, try it at Your own risk:
  * [FreeTuxTv.net](http://database.freetuxtv.net)
  * [IPTV-Player.com](http://iptv-player.com/?id=database)
  * [HasBahCaIPTV.com](http://hasbahcaiptv.com/index.php?dir=m3u)
  * [IPTV-Tv.blogspot.com](http://iptv-tv.blogspot.com)
  * [TvOnlineStreams.com](http://www.tvonlinestreams.com)
  * [Plex forums](http://forums.plex.tv/discussion/83083/rel-iptv-bundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/p1)
  * [Google.com](http://lmgtfy.com/?q=iptv+m3u)

Playlist supports additional attributes that can be optionally defined inline after #EXTINF:0 and before the name of the media:
  * **tvg-id**, **tvg-name** - used to identify channel in [XMLTV][4];
  * **tvg-logo**, **logo** - stream logo or icon, can use remote media (url must include http part) or stored images from *\IPTV.bundle\Content\Resources* folder (filename must include extension);
  * **group-title** - category name;
  * **group-logo** - category logo, only usable in first line where specific category is defined, in example if You have two channels with same category name, logo supplied in first line of those two will be used.

A simple example (see included sample playlist for more):
```
#EXTM3U
#EXTINF:0 tvg-id="Cartoon Network" tvg-logo="icon-default.png" group-title="Cartoons" group-logo="icon-folder.png",Cartoon Network
http://80.87.146.133:1111/udp/230.3.3.112:5678
#EXTINF:-1 tvg-logo="http://www.lyngsat-logo.com/hires/mm/mtv_dance_us.png" group-title="Music",MTV Dance
http://80.87.146.133:1111/udp/230.3.3.115:5678
```

At the moment this plugin is [unable to handle multiple playlists][8], but it is possible to have [multiple instances of this plugin](https://github.com/Cigaras/IPTV.bundle/issues/21#issuecomment-159568329) and use different playlist for each, not the prettiest way but it is a solution.

Read further for more information about [supported protocols and required configurations][6].

### Program guide ###
As of version 1.2 and further this plugin supports [program guide](http://en.wikipedia.org/wiki/Electronic_program_guide) in [XMLTV](https://en.wikipedia.org/wiki/XMLTV) format, there is a sample located in *IPTV.bundle\Content\Resources\guide.xml*, you can specify other filename in preferences, but You can not specifify a path outside resources forder because Plex prohibits it. Online guide is also supported (as long as it matches the [XMLTV](https://en.wikipedia.org/wiki/XMLTV) format), You just need to specify a direct link to it, with http part included.

Plugin will try to match the program guide with playlist streams by the stream title, but to make things easier **tvg-id** atribute might be used to represent the exact XMLTV channel, for example if XMLTV looks something like this:
```
<tv>
  ...
  <programme start="20160321031000 +0200" stop="20160321040100 +0200" channel="Cartoon Network RSE">
    ...
  </programme>
  ...
</tv>
```
then previously [mentioned][3] playlist should look like this:
```
#EXTM3U
#EXTINF:0 tvg-id="Cartoon Network RSE" tvg-logo="icon-default.png" group-title="Cartoons",Cartoon Network
http://80.87.146.133:1111/udp/230.3.3.112:5678
...
```

Recomended software for XMLTV generation would be [**WebGrab+Plus**](http://www.webgrabplus.com/), please refer to its [documentation](http://www.webgrabplus.com/documentation/quick-start) on how to set it up.

Please note, program guide is quite demanding on resources and I do not recomend using XMLTV file that has more channels than You actualy need and the shorter the period its generated for the better.

### Compatible devices and limitations ###
By default Plex Media Server [does](http://forums.plex.tv/discussion/84637/problems-getting-live-http-stream-into-channel) [not](https://forums.plex.tv/discussion/comment/475261#Comment_475261) transcode live streams and leaves this job to clients. In some clients it is possible to **switch [Direct Play and Direct Streaming](https://support.plex.tv/hc/en-us/articles/200250387-Streaming-Media-Direct-Play-and-Direct-Stream) off** and then server will do the heavy lifting, but some clients are out of luck and will only play streams they are able to handle natively.

Here is a bunch of Plex clients and some testing results, keep in mind that apps are beeing updated constantly and folowing list might (and usualy will) be outdated:

* **Desktop apps**:
  * **[Plex Media Center]** - no longer in production but you can get one from ~~[old Plex Wiki page](https://oldwiki.plexapp.com/index.php?title=Downloads#Plex_Media_Center_.28PMC_-_standalone_client.29)~~  [Plex Downloads Archive][Plex Media Center] or [cnet.com](http://download.cnet.com/Plex-Media-Center/3000-2139_4-75754342.html), plays [most streams][6] without problems, latest known version 0.9.5.4;
  * **[Plex Home Theater][GetPlex]** - [HTTP][6] streams work, tested on version 1.4.1, not sure about other [protocols][6];
  * **[Plex Media Player](https://blog.plex.tv/2015/10/20/introducing-the-plex-media-player/)** - [HTTP][6] streams [work](https://github.com/Cigaras/IPTV.bundle/issues/41), tested by [Codehhh](https://github.com/Codehhh), not sure about other [protocols][6];
  * **[Plex Web]** - most streams require turning off [Direct Play and Direct Stream](https://support.plex.tv/hc/en-us/articles/200250387-Streaming-Media-Direct-Play-and-Direct-Stream) in [Settings->Web->Player](https://github.com/Cigaras/IPTV.bundle/commit/cd0b1b35921c80993856d2a0d2ef42a119a84565#commitcomment-17552365));
* **Connected devices**:
  * **[Plex for Xbox][GetPlex]** - did not work for [Be4stElectrjc](https://github.com/Cigaras/IPTV.bundle/commit/3f420423e2c02d3fe86d0b1eb99527a4af0e57b6#commitcomment-17536080);
  * **[Plex for PlayStation][GetPlex]** - not tested;
  * **[Plex for Apple TV][GetPlex]** - not tested;
  * **[PlexConnect](https://forums.plex.tv/categories/appletv-plexconnect) (old Apple TV)** - [many](https://forums.plex.tv/discussion/comment/496660#Comment_496660) [users](https://forums.plex.tv/discussion/comment/496683#Comment_496683) [report](https://forums.plex.tv/discussion/comment/538729#Comment_538729) [that it](https://forums.plex.tv/discussion/comment/545983#Comment_545983) does work, You just need to alternate between transcoding options, or [use third party transcoding service](https://forums.plex.tv/discussion/comment/539331#Comment_539331);
  * **[Plex for Chromecast][GetPlex]** - not tested;
  * **[Plex for Amazon Fire TV][GetPlex]** - not tested;
  * **[Plex for Roku][GetPlex]** - for some it [works](https://forums.plex.tv/discussion/comment/502904#Comment_502904), for some it [does not](https://forums.plex.tv/discussion/comment/482524#Comment_482524), [wheezycheezel](https://forums.plex.tv/profile/wheezycheezel) posted [step by step guide](https://forums.plex.tv/discussion/comment/544372#Comment_544372) for [TVHeadend](https://tvheadend.org/) streams on [Plex forums](https://forums.plex.tv/discussion/comment/544372#Comment_544372), needs more [testing][7];
  * **[Plex for Android TV][GetPlex]** - not tested;
  * **[Plex for Samsung][GetPlex]** - works for [MACE-Zer0](https://github.com/Cigaras/IPTV.bundle/issues/29) but apparently nobody else;
  * **[Plex for Vizio][GetPlex]** - not tested;
  * **[Plex for Opera TV][GetPlex]** - not tested;
  * **Plex for LG TV ([MediaLink])** plays [HTTP and RTSP][6] streams, however MediaLink is no longer included LG products of year 2013 and later, [Simon J. Hogan](https://forums.plex.tv/discussion/89004) is working on a [Plex client for LG Smart TV](http://simonjhogan.github.io/plex.lg/), however I did not test it;
* * **Mobile devices**:
  * **[Plex for Android][GetPlex]** - usualy does not work, should work with external player like [MX Player](https://play.google.com/store/apps/details?id=com.mxtech.videoplayer.ad), needs [testing][7];
  * **[Plex for iOS][GetPlex]** - [at the moment does not play any streams at all](https://forums.plex.tv/discussion/comment/536311#Comment_536311);
  * **[Plex for Windows Phone][GetPlex]** - not tested;

You can test your client by putting stream url into a \*.strm file and loading it into Plex as Home Video as mentioned [above][1] and [below][7].

Also You can try running a dedicated transcoding service and get Your streams in [preferable format](https://forums.plex.tv/discussion/comment/539331#Comment_539331), [VODServer] is a good and free example.

One more flaw of this plugin is that it has no control over audio tracks if stream has multiple. Some clients can change the track, some can not, but plugin can not predefine one and I have [no solution](https://forums.plex.tv/discussion/85178) at the moment.

Read [further][6] for specific configuration required for some streaming protocols.

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

Keep in mind that all streams are unique and Plex will not be able to play all of them, but not necessary because of plugins fault (read [Compatible devices and limitations][5]). Please try playing stream with [VLC] and using \*.strm file method described [above][5] and [below][7] before blaming this plugin. If \*.strm method works and plugin does not, please [contact me][9].

### Troubleshooting ###
If You encounter errors or some streams do not work please do the following:

1. Try disabling [Direct Play and Direct Stream](https://support.plex.tv/hc/en-us/articles/200250387-Streaming-Media-Direct-Play-and-Direct-Stream) in Your client settings, this helps 9 of 10 times. However some clients do not have these settings, if You're the unlucky one or this does not help, continue to next step:

2. Make sure the playlist file is [encoded in UTF-8 without BOM][6];

3. Try to play the stream in [VLC] player, if it fails Your stream is invalid and will not play on any device; if it works continue to next step:

4. Create a new file with notepad, write your desired streams url there and save it with \*.strm extension, put it into a folder and load folder into Plex Server as Home Video, try to play it in Plex client (preferably [Plex Media Center][5] because Plex Home Theater as of version 1.4.1 does not like \*.strm files), if it fails, then usualy Your client is unable to play this stream, try alternative clients; if it works, continue to next step:

5. Check plugin log file *com.plexapp.plugins.iptv.log*, refer to official Plex support page [Plex Media Server Log Files](https://support.plex.tv/hc/en-us/articles/200250417-Plex-Media-Server-Log-Files) for log file location.

6. If You do not have a solution after checking the log file, submit a [ticket on GitHub](https://github.com/Cigaras/IPTV.bundle/issues/new) or post on [Plex forum](http://forums.plex.tv/discussion/83083/rel-iptv-bundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/p1) with log and playlist files attached and I or other users will try to help You.

### To do list ###
* Support multiple playlists (for the moments it is possible to make [multiple instances of this plugin](https://github.com/Cigaras/IPTV.bundle/issues/21#issuecomment-159568329) and use different playlist for each);
* Improve the program guide;
* Possibility to predefine audio track, if ever becomes possible.

### Credits and contacts ###
* Developer: [Valdas Vaitiekaitis], also known as [Cigaras];
* Contributors: [supergivi](https://github.com/supergivi), [sander1](https://github.com/sander1), [Funtic](https://github.com/Funtic), [skyglow](https://github.com/skyglow) and many others;
* [Artwork](http://www.flickr.com/photos/purplesherbet/10579021143) by photographer D. Sharon Pruitt, owner of [Purple Sherbet Photography](http://www.flickr.com/photos/purplesherbet/), licensed under [CC Attribution 2.0](http://creativecommons.org/licenses/by/2.0);
* [Icons](http://www.iconarchive.com/show/ultrabuuf-icons-by-mattahan.html) by artist Paul Davey, also known as [Mattahan](http://mattahan.deviantart.com/), licensed under [CC Attribution-Noncommercial-Share Alike 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0);
* Advisors: [shopgirl284](http://forums.plexapp.com/index.php/user/87889-shopgirl284/), [Mikedm139](http://forums.plexapp.com/index.php/user/14450-mikedm139/).

If You have any questions or suggestions, please feel free to contact me via [GitHub](https://github.com/Cigaras) or [Plex forum](https://forums.plex.tv/discussion/83083), or visit my personal blog at [cigaras.blogspot.lt](http://cigaras.blogspot.lt), but please keep in mind that I did this plugin voluntary and I have other priorities to do. However if You find my work useful, please consider a small [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted) as a sign of gratitude and support.

### License ###
Copyright © 2013-2016 Valdas Vaitiekaitis

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

  [1]: #introduction "Introduction"
  [2]: #installation "Installation"
  [3]: #playlist-structure-and-examples "Playlist structure and examples"
  [4]: #program-guide "Program guide"
  [5]: #compatible-devices-and-limitations "Compatible devices and limitations"
  [6]: #supported-protocols "Supported protocols"
  [7]: #troubleshooting "Troubleshooting"
  [8]: #to-do-list "To do list"
  [9]: #credits-and-contacts "Credits and contacts"
  [10]: #license "License"
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
