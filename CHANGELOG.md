Version 1.2.3 (2016-07-19)
* Implemented a method to correctly observe the timezone UTC offset in the XMLTV guide if it exists by [Lee](https://github.com/Cigaras/IPTV.bundle/commit/181169aeacfc5ee3af3e91a41cd12ad94afafb6f)
* Fix for RasPlex issue by [Strux](https://github.com/Cigaras/IPTV.bundle/commit/40056ecbdcfc41de27d3ad36d287b4cc84a49345)

Version 1.2.2 (2016-03-30)
* Fixed issue [#39](https://github.com/Cigaras/IPTV.bundle/issues/39) by [skyglow](https://github.com/skyglow)

Version 1.2.1 (2016-03-24)
* Fixed issue [#22](https://github.com/Cigaras/IPTV.bundle/issues/22)

Version 1.2.0 (2016-03-23)
* Rewritten program guides parsing, now should work much faster, but still quite demanding
* Added group logo, refer to [README.MD](https://github.com/Cigaras/IPTV.bundle#program-guide) file for more details
* Group sorting fix

Version 1.1.0 (2016-03-21)
* Added program guide support, please refer to [README.MD](https://github.com/Cigaras/IPTV.bundle#program-guide) file for more details

Version 1.0.11 (2015-12-11)
* Optimization by Funtic
  * Moved playlist loading to separate method and optimized menu creation process
  * Added ability to return custom default value if Attribute is not set
  * Cleared duplicate group names localization

Version 1.0.10 (2015-02-11)
* Partialy disabled webkit players by [sander1](https://github.com/sander1), RTMP webkit player still will be used if Real RTMP is enabled in Preferences but disabled in Info.plist file, by default both are disabled for compatibility with older clients, please refer to [README.MD](https://github.com/Cigaras/IPTV.bundle#supported-protocols) file for more details
* Updated documentation ([README.MD])

Version 1.0.9 (2014-02-07)
* Sorting fix
* Minor optimization

Version 1.0.8 (2014-02-06)
* Disable/enable sorting in preferences

Version 1.0.7 (2014-02-01)
* HTTPS playlist fix, dropbox playlists work now

Version 1.0.6 (2013-12-30)
* More fixes by [supergivi](https://github.com/supergivi):
  * Duplicate playlist entries fix
  * Unicode better fix
  * Removed unnecessary group title localizations
* Switch from global lists to local dictionaries because with global list playlist change requires server restart when with local dictionary only plugin must be relaunched on client side
* Updated documentation ([README.MD])

Version 1.0.5 (2013-12-23):
* Cyrilic group-title fix by [supergivi](https://github.com/supergivi)

Version 1.0.4 (2013-12-20):
* Items list array moved from local variable to global because of compatibility issues with some devices

Version 1.0.3 (2013-12-12):
* Undefined logos fix for some devices

Version 1.0.2:
* Trying to fix undefined logos for some devices

Version 1.0.1 (2013-11-07):
* Endless recursion of CreateVideoClipObject for compatibility with LG Smart TV

Version 1.0 (2013-11-07):
* Release version
* Code clean up
* New artwork and icons

Version 0.9 RC1 (2013-11-04):
* Local logos
* Code clean up
* Better documentation ([README.MD])

Version Beta3 (2013-10-30):
* Online playlist
* RTMP custom player support (full url)
* Localisation (EN only at the moment)

Version Beta2 (2013-10-22):
* RTMP, MMS compatibility
* Preferences

Version Beta1 (2013-10-11):
* HTTP, RTSP streaming
* Customisable playlist with groups and logos

  [README.MD]: https://github.com/Cigaras/IPTV.bundle#plex-media-server-plugin-to-play-network-streams-aka-iptv-from-a-m3u-playlist
