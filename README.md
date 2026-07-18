# IPTV Sardegna

Playlist IPTV dei canali TV regionali della Sardegna, basata sugli stream
pubblici che le emittenti trasmettono ufficialmente sui propri siti web.

Playlist principale: [`1628947598916_canali_tv_sardegna.m3u`](1628947598916_canali_tv_sardegna.m3u)

## Come funziona

La maggior parte dei canali usa un normale URL HLS (`.m3u8`) stabile.

**Videolina**, **Sardegna 1** e **L'Unione TV** (canale del gruppo L'Unione
Sarda, lo stesso di Videolina) trasmettono invece la diretta ufficiale
tramite Dailymotion, i cui URL HLS contengono un token temporaneo che scade
dopo alcune ore. Per questo motivo:

- la playlist principale punta ai file in [`streams/`](streams/) di questo
  repository (tramite `raw.githubusercontent.com`);
- la GitHub Action
  [`refresh-streams.yml`](.github/workflows/refresh-streams.yml) rigenera
  quei file **ogni 4 ore** eseguendo
  [`scripts/refresh_dailymotion.py`](scripts/refresh_dailymotion.py), che
  ricava l'URL tokenizzato corrente dal player pubblico Dailymotion usato
  dai siti ufficiali delle emittenti.

> **Nota**: il workflow pianificato gira solo sul branch predefinito
> (`main`). Dopo il merge è possibile lanciarlo subito a mano dalla tab
> *Actions* → *Aggiorna stream Dailymotion* → *Run workflow*. Su repository
> pubblici GitHub disabilita i workflow pianificati dopo 60 giorni senza
> attività: in tal caso basta riabilitarlo dalla tab Actions.

## Stato dei canali (verifica del 2026-07-18)

| Canale | Stato | Fonte |
| --- | --- | --- |
| Videolina | ✅ verificato (via Dailymotion, auto-aggiornato) | [videolina.it/live](https://www.videolina.it/live) |
| L'Unione TV | ✅ verificato (via Dailymotion, auto-aggiornato) | gruppo L'Unione Sarda |
| Sardegna 1 | ✅ verificato (via Dailymotion, auto-aggiornato) | [sardegna1.it/live/diretta-live](https://www.sardegna1.it/live/diretta-live/) |
| Tele Costa Smeralda | ✅ verificato | HLS diretto |
| TeleSardegna | ✅ verificato | HLS diretto (MainStreaming, da [telesardegna.it](https://www.telesardegna.it/)) |
| Radio Televisione Sarda | ✅ verificato | HLS diretto |
| Tele Radio Maristella | ✅ verificato | HLS diretto |
| Radiolina TV | ✅ verificato (via Dailymotion, auto-aggiornato) | [radiolina.it](https://www.radiolina.it/) — visual radio del gruppo Videolina |
| Radio Iglesias TV | ✅ verificato | HLS diretto |
| Aristanis TV (ex Super TV Oristano) | ⚠️ non verificabile dall'ambiente di test (porta 1936); link attuale censito da [Zappr](https://github.com/ZapprTV/channels) | HLS diretto |
| Uno4 TV | ⚠️ il CDN ufficiale (`cdn.uno4.it`) rispondeva 502 al momento della verifica; link lasciato perché è quello ufficiale corrente | HLS diretto |
| Radio OndaSarda | ⚠️ non verificabile dall'ambiente di test (porta 1936); voce commentata in playlist | HLS diretto |
| Teleregione Live | ℹ️ solo Twitch (`teleregione_sardegna`), commentato in playlist | Twitch |
| Canale 48 Sardegna | ℹ️ solo Twitch (`canale48webtv`), commentato in playlist | Twitch |
| EjaTV | ℹ️ solo YouTube, commentato in playlist | [ejatv.com](https://www.ejatv.com/) |
| Catalan TV (Alghero) | ℹ️ solo YouTube, commentato in playlist | [catalantv.it](https://www.catalantv.it/diretta/) |
| Bonaria TV | ℹ️ solo YouTube, commentato in playlist | TV Corallo |

Canali rimasti fuori: **YouTg** (rimosso: il link disponibile è un
contenuto on-demand del player del sito, non una vera diretta),
**Odeon 24 Sardegna** (server irraggiungibile),
**Sardegna Live** (player Livepush con URL generato dinamicamente, non
collegabile in modo stabile da una playlist statica), **TTS** e
**Canale Italia Sardegna** (nessuno stream ufficiale pubblico: esistono solo
restream di terze parti del segnale DTT).

## Legalità

Tutti i link puntano agli stream pubblici e gratuiti che le emittenti
stesse distribuiscono ufficialmente (sui propri siti, su Dailymotion o su
Twitch). Nessun contenuto è ospitato in questo repository.
