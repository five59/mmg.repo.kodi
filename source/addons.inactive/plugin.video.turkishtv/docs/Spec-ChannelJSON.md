# mmg-kodi / docs / Spec-ChannelJSON

## Top-Level Keys

Key | Format | Value
--- | ------ | -----
**LabelStringID** | String | Numeric identifier found in the language resource files (under resources/language/*/strings.xml).
**Icon** | String (URL or File Path) | if relative file path, points to resources/media/icon.
**FanArt** | String (URL or File Path) | if relative file path, points to resources/media/fanart.
**Data** | Array | Array of available channels

## Data Array Keys
Key | Format | Required | Value
--- | ------ | -------- | -----
**Label** | String | Yes | Name of the channel. Displayed to user.
**Icon** | String (URL or File Path) | Yes | If relative file path, points to resources/media/icon.
**StreamType** | String | Yes | Currently "Stream" only, representing a video stream that is handled by Kodi with a simple URL. Future development may include support for DailyMotion, uStream, Akamai CDN and other video streaming services requiring additional support to play.
**URL** | String (URL) | Yes | The URL (playable by Kodi) for the video stream. Currently supports http playlists (.m3u8) and RTMP.
**Active** | Integer | Yes | 0 to disable, 1 to enable.
