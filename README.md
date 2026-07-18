# IPTV Sardegna

An IPTV playlist containing public, official web streams of regional TV channels from Sardinia, Italy.

## Playlist Link

To use this playlist, copy the URL below and paste it into your favorite IPTV player (such as VLC, Kodi, TiviMate, or other IPTV applications):

```text
https://raw.githubusercontent.com/amgothic80/iptv-sardegna/main/1628947598916_canali_tv_sardegna.m3u
```

## How It Works

* **Direct Streams:** Most channels stream using stable, direct HLS URLs (`.m3u8`).
* **Dynamic Streams (Dailymotion):** Broadcasters such as **Videolina**, **Sardegna 1**, **L'Unione TV**, and **Radiolina TV** stream officially via Dailymotion. These streams contain temporary security tokens that expire after a few hours.
* **Auto-Update:** A scheduled GitHub Action runs automatically every 4 hours to extract the latest streaming tokens and keep the playlist files inside the `streams/` directory updated.

## Channel List

| Channel | Stream Source | Quality |
| --- | --- | --- |
| Videolina | Dailymotion (auto-updated) | Up to 720p HD |
| L'Unione TV | Dailymotion (auto-updated) | Up to 720p HD |
| Sardegna 1 | Dailymotion (auto-updated) | Up to 720p HD |
| Radiolina TV | Dailymotion (auto-updated) | Up to 720p HD |
| Tele Costa Smeralda | Direct HLS | 720p |
| TeleSardegna | Direct HLS | 1080p |
| Radio Televisione Sarda | Direct HLS | 1080p |
| Tele Radio Maristella | Direct HLS | 1080p |
| Radio Iglesias TV | Direct HLS | SD |
| Aristanis TV | Direct HLS | SD |
| Uno4 TV | Direct HLS | SD |

## Legal Disclaimer

All stream links point directly to the official, free-to-air web streams distributed by the broadcasters themselves. No copyrighted video content is hosted, stored, or re-transmitted within this repository.
