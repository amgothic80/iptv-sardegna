#!/usr/bin/env python3
"""Scheduler per refresh automatico dei token Dailymotion.

Esegue il refresh ogni 4 ore. Ideale per Termux su smartphone
che rimane quasi sempre acceso.

Utilizzo:
  python3 run_cron.py        # Avvia scheduler (ogni 4 ore)
  python3 run_cron.py --once # Esegui refresh una volta
"""

import subprocess
import sys
import time
from datetime import datetime


def run_refresh():
    """Esegue refresh_dailymotion.py e committa i cambiamenti."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Avvio refresh...")
    try:
        # Esegui lo script di refresh
        subprocess.run(
            ["python3", "scripts/refresh_dailymotion.py"],
            check=True,
            capture_output=True,
        )

        # Aggiungi i file modificati
        subprocess.run(["git", "add", "streams/"], check=True)

        # Verifica se ci sono cambiamenti
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True,
        )

        if result.returncode != 0:
            # Ci sono cambiamenti, fai il commit
            subprocess.run(
                ["git", "commit", "-m", "Aggiorna token stream Dailymotion"],
                check=True,
                capture_output=True,
            )
            # Push al repository
            subprocess.run(["git", "push"], check=True, capture_output=True)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Refresh completato e pushato")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ℹ️ Nessuna modifica ai token")

    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Errore: {e}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Errore inatteso: {e}")


def main():
    """Loop principale che esegue il refresh ogni 4 ore, o una sola volta con --once."""
    # Controlla argomenti da linea di comando
    run_once = "--once" in sys.argv

    if run_once:
        print("🔄 Esecuzione singola del refresh")
        run_refresh()
        print("✅ Refresh completato")
    else:
        print("🚀 Scheduler Dailymotion avviato")
        print("⏰ Refresh programmato ogni 4 ore")
        print("💡 Mantieni Termux aperto per il funzionamento continuo")
        print()

        # Esegui il primo refresh subito
        run_refresh()

        # Poi continua ogni 4 ore (14400 secondi)
        while True:
            print(f"⏳ Prossimo refresh tra 4 ore ({datetime.now().strftime('%H:%M:%S')})")
            time.sleep(14400)  # 4 ore in secondi
            run_refresh()


if __name__ == "__main__":
    main()
