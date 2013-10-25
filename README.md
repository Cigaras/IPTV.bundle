#### Plex Media Server plugin to play network streams (a.k.a. IPTV) from a M3U playlist ####
Version Beta2

- - -
For those who do not know what Plex is - it is a media server solution allowing You to access Your media from multiple different devices, and my addon pushes it even further - it lets You watch network streams from all over the world! All You need is a [Plex Server](http://www.plexapp.com/getplex/), a device with [Plex App](http://www.plexapp.com/getplex/) on it and a playlyst of Your favorite streams (Some limitations apply, please read below).

Playlist must be generated using M3U standards (http://en.wikipedia.org/wiki/M3U), stored in Contents\Resources folder and named playlist.m3u (name can be changed in Preferences), there are some additional attributes supported:
* tvg-logo;
* group-title.

In included sample playlist some streams may not work, but should serve well as an example on how to fill Your own playlist. You can find many public streams at [freetuxtv.net](http://database.freetuxtv.net/) and [iptv-player.com](http://iptv-player.com/?id=database) or just use Google. Plugin tested on:
* Plex Media Center for PC v.0.9.5.4;
* LG 42LW650s TV;
* Plex/Web (Plex Media Server v.0.9.8.6).

Working/not working protocols:
* [HTTP](http://en.wikipedia.org/wiki/HTTP_Live_Streaming) - should work on all devices natively;
* [RTSP](http://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol) - should work on all devices natively;
* [RTMP](http://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol) - uses [Plex's hosted RTMP player](http://www.plexapp.com/player/player.php), works on [desktop clients](http://www.plexapp.com/desktop/), but plugin becomes incompatible with most other devices so functionality is disabled by default and plugin will try to play RTMP videos over HTTP protocol (some streams work this way), You can enable it in Preferences, but You need to manualy uncomment 14th line in Info.plist file to enable "UseRealRTMP";
* [MMS](http://en.wikipedia.org/wiki/Microsoft_Media_Server) - uses [Plex's hosted Silverlight player](http://www.plexapp.com/player/silverlight.php), did not work on tested devices so functionality is disabled by default and plugin will try to play MMS videos over HTTP protocol, You can enable it in Preferences;

Planned for the future:
* online playlist;
* [EPG](http://en.wikipedia.org/wiki/Electronic_program_guide);
* custom SWF players support;
* [MMS](http://en.wikipedia.org/wiki/Microsoft_Media_Server) protocol/player troubleshooting;
* Plex Services.


If You have any questions or suggestions, please feel free to contact me via GitHub or [PlexApp forum](http://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/). If You find my work usefull, please concider a small [donation via PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted).

- - -
Copyright (c) 2013 Valdas Vaitiekaitis, a.k.a. [Cigaras](http://forums.plexapp.com/index.php/user/107872-cigaras/). All rights reserved.
