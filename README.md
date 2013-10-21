#### Plex Media Server plugin to play network streams (a.k.a. IPTV) from a M3U playlist ####
version 1.0 RC1

- - -
Playlist must be generated using M3U standarts (http://en.wikipedia.org/wiki/M3U), stored in Contents\Resources folder and named playlist.m3u, there are some additional attributes supported:
* tvg-logo;
* group-title.

Working/not working streams:
* HTTP - working;
* [RTSP](http://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol) - working;
* [RTMP](http://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol) - some work, some do not;
* [MMS](http://en.wikipedia.org/wiki/Microsoft_Media_Server)/MMSH - not working;

In included sample playlist some streams may not work, but should serve well as an example. You can find many public streams at [freetuxtv.net](http://database.freetuxtv.net/) or just use Google. Should work on any client that is capable of playing desired network streams. Tested on:
* Plex Media Center for PC v.0.9.5.4
* LG 42LW650s TV

Planned for the future:
* RTMP fixes and MMS/MMSh support;
* multi language support;
* configurable playlist name, possibility to use online playlist;
* [EPG](http://en.wikipedia.org/wiki/Electronic_program_guide).


If you have any questions or suggestions, please feel free to contact me via GitHub or [PlexApp forum](http://forums.plexapp.com/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/). If you find my work usefull, please concider a small [donation via PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Cigaras%40gmail%2ecom&lc=LT&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted).

- - -
Copyright (c) 2013 Valdas Vaitiekaitis, a.k.a. [Cigaras](http://forums.plexapp.com/index.php/user/107872-cigaras/). All rights reserved.
