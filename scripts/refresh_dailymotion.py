#!/usr/bin/env python3
"""Aggiorna i file streams/*.m3u8 dei canali che trasmettono su Dailymotion.

Videolina, Sardegna 1 e L'Unione TV pubblicano la diretta ufficiale tramite
il player Dailymotion incorporato nei rispettivi siti. Gli URL HLS di
Dailymotion contengono un token temporaneo ("sec="), quindi vanno
rigenerati periodicamente: questo script interroga l'endpoint pubblico dei
metadati del player e salva il master playlist HLS corrente in streams/.
"""

import json
import sys
import urllib.request
from pathlib import Path

# nome file -> ID del video live Dailymotion (dal player del sito ufficiale)
CHANNELS = {
    "videolina": "k5IzEKA6K34xZiEXbVm",   # www.videolina.it/live
    "sardegna1": "x893du6",               # www.sardegna1.it/live/diretta-live
    "unione-tv": "k58ADHSu6a0wFJGfQnC",   # L'Unione TV (gruppo L'Unione Sarda)
}

# Il CDN di Dailymotion risponde 403 agli user-agent browser completi
# inviati da client non-browser: quello generico invece è accettato.
USER_AGENT = "Mozilla/5.0"

STREAMS_DIR = Path(__file__).resolve().parent.parent / "streams"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def refresh(name: str, video_id: str) -> bool:
    meta = json.loads(
        fetch(f"https://www.dailymotion.com/player/metadata/video/{video_id}")
    )
    qualities = meta.get("qualities") or {}
    entries = qualities.get("auto") or []
    if not entries or not entries[0].get("url"):
        raise RuntimeError(f"nessun URL HLS nei metadati di {video_id}")
    master_url = entries[0]["url"]
    master = fetch(master_url)
    if not master.startswith("#EXTM3U"):
        raise RuntimeError(f"il master playlist di {video_id} non è HLS valido")
    (STREAMS_DIR / f"{name}.m3u8").write_text(master, encoding="utf-8")
    return True


def main() -> int:
    STREAMS_DIR.mkdir(exist_ok=True)
    failures = []
    for name, video_id in CHANNELS.items():
        try:
            refresh(name, video_id)
            print(f"[ok] {name}")
        except Exception as exc:  # noqa: BLE001 - il canale può essere offline
            # In caso di errore il file precedente resta invariato.
            failures.append(name)
            print(f"[errore] {name}: {exc}", file=sys.stderr)
    # Fallisce solo se nessun canale è stato aggiornato.
    return 1 if len(failures) == len(CHANNELS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
