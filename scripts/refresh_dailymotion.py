#!/usr/bin/env python3
"""Aggiorna i file streams/*.m3u8 dei canali che trasmettono su Dailymotion.

Videolina, Sardegna 1, L'Unione TV e Radiolina pubblicano la diretta
ufficiale tramite il player Dailymotion incorporato nei rispettivi siti.
Gli URL HLS di Dailymotion contengono un token temporaneo ("sec="), quindi
vanno rigenerati periodicamente: questo script interroga l'endpoint
pubblico dei metadati del player e salva il master playlist HLS corrente
in streams/.

Nota importante sulla qualità: quando il master viene richiesto da un IP
di datacenter (come questo script o i runner GitHub), Dailymotion elenca
solo le varianti a bassa risoluzione (380/240), ma sul CDN esistono anche
le varianti superiori (tipicamente 480 e 720), raggiungibili con lo stesso
token sostituendo il nome della rendition nell'URL. Lo script quindi sonda
tutte le rendition note e ricostruisce un master completo con l'HD in
cima, così i player scelgono la qualità migliore davvero disponibile.
"""

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

# nome file -> ID del video live Dailymotion (dal player del sito ufficiale)
CHANNELS = {
    "videolina": "k5IzEKA6K34xZiEXbVm",   # www.videolina.it/live
    "sardegna1": "x893du6",               # www.sardegna1.it/live/diretta-live
    "unione-tv": "k58ADHSu6a0wFJGfQnC",   # L'Unione TV (gruppo L'Unione Sarda)
    "radiolina": "k2KONW2dOh2PqAGfWS4",   # www.radiolina.it (visual radio del gruppo)
}

# rendition Dailymotion -> (RESOLUTION, BANDWIDTH stimata in bit/s)
# dall'alto verso il basso: i player partono in genere dalla prima voce
RENDITIONS = {
    "2160": ("3840x2160", 12000000),
    "1080": ("1920x1080", 5500000),
    "720": ("1280x720", 2800000),
    "480": ("854x480", 1500000),
    "380": ("512x288", 800000),
    "240": ("320x180", 500000),
}

# Il CDN di Dailymotion risponde 403 agli user-agent browser completi
# inviati da client non-browser: quello generico invece è accettato.
USER_AGENT = "Mozilla/5.0"

# Dai runner di GitHub Actions (IP noti di datacenter) Dailymotion può
# restituire 403 in modo intermittente. Inviare Referer/Origin come farebbe
# il player incorporato riduce i falsi positivi dell'anti-bot; in aggiunta
# si ritenta con un breve backoff prima di arrendersi.
HEADERS = {
    "User-Agent": USER_AGENT,
    "Referer": "https://www.videolina.it/",
    "Origin": "https://www.videolina.it",
}
RETRY_DELAYS = (0, 2, 5)

STREAMS_DIR = Path(__file__).resolve().parent.parent / "streams"


def fetch(url: str) -> str:
    last_error = None
    for delay in RETRY_DELAYS:
        if delay:
            time.sleep(delay)
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:  # noqa: BLE001 - si ritenta, poi si propaga
            last_error = exc
    raise last_error


def is_valid_playlist(url: str) -> bool:
    try:
        return fetch(url).startswith("#EXTM3U")
    except Exception:  # noqa: BLE001 - 404/timeout = rendition assente
        return False


def refresh(name: str, video_id: str) -> None:
    meta = json.loads(
        fetch(f"https://www.dailymotion.com/player/metadata/video/{video_id}")
    )
    qualities = meta.get("qualities") or {}
    entries = qualities.get("auto") or []
    if not entries or not entries[0].get("url"):
        raise RuntimeError(f"nessun URL HLS nei metadati di {video_id}")
    master = fetch(entries[0]["url"])
    if not master.startswith("#EXTM3U"):
        raise RuntimeError(f"il master playlist di {video_id} non è HLS valido")

    variants = [l.split("#cell")[0] for l in master.splitlines() if l.startswith("https")]
    template = variants[0] if variants else ""
    lines = ["#EXTM3U"]
    if template and re.search(r"live-\d+", template):
        for quality, (resolution, bandwidth) in RENDITIONS.items():
            candidate = re.sub(r"live-\d+", f"live-{quality}", template)
            if is_valid_playlist(candidate):
                lines.append(
                    f"#EXT-X-STREAM-INF:RESOLUTION={resolution},"
                    f'FRAME-RATE=25.000000,BANDWIDTH={bandwidth},NAME="{quality}"'
                )
                lines.append(candidate)
    if len(lines) > 1:
        content = "\n".join(lines) + "\n"
        best = lines[1].split("RESOLUTION=")[1].split(",")[0]
        print(f"[ok] {name} (fino a {best})")
    else:
        # sonda fallita: meglio il master originale che niente
        content = master
        print(f"[ok] {name} (master originale, sonda rendition fallita)")
    (STREAMS_DIR / f"{name}.m3u8").write_text(content, encoding="utf-8")


def main() -> int:
    STREAMS_DIR.mkdir(exist_ok=True)
    failures = []
    for name, video_id in CHANNELS.items():
        try:
            refresh(name, video_id)
        except Exception as exc:  # noqa: BLE001 - il canale può essere offline
            # In caso di errore il file precedente resta invariato.
            failures.append(name)
            print(f"[errore] {name}: {exc}", file=sys.stderr)
    # Fallisce solo se nessun canale è stato aggiornato.
    return 1 if len(failures) == len(CHANNELS) else 0


if __name__ == "__main__":
    raise SystemExit(main())

