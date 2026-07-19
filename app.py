#!/usr/bin/env python3
"""Web interface per refresh automatico token Dailymotion.

Fornisce una pagina web semplice con un pulsante per aggiornare i token.
Ideale per Termux su smartphone.

Avvio:
  python3 app.py

Accesso:
  http://localhost:5000
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates', static_folder='static')
STREAMS_DIR = Path(__file__).parent / 'streams'


def get_channel_status():
    """Ritorna lo stato di aggiornamento dei canali."""
    channels = {
        'videolina': STREAMS_DIR / 'videolina.m3u8',
        'sardegna1': STREAMS_DIR / 'sardegna1.m3u8',
        'unione-tv': STREAMS_DIR / 'unione-tv.m3u8',
        'radiolina': STREAMS_DIR / 'radiolina.m3u8',
    }

    status = {}
    for name, path in channels.items():
        if path.exists():
            mtime = path.stat().st_mtime
            dt = datetime.fromtimestamp(mtime)
            status[name] = {
                'updated': dt.isoformat(),
                'display': dt.strftime('%d/%m/%Y %H:%M')
            }
        else:
            status[name] = {
                'updated': None,
                'display': 'Mai aggiornato'
            }

    return status


def format_time_ago(iso_string):
    """Converte timestamp ISO a formato "X ore fa", "X giorni fa", etc."""
    if not iso_string:
        return "Mai"

    dt = datetime.fromisoformat(iso_string)
    now = datetime.now()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return "Pochi secondi fa"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minuto/i fa"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} ora/e fa"
    else:
        days = int(seconds / 86400)
        return f"{days} giorno/i fa"


@app.route('/')
def index():
    """Pagina principale con pulsante refresh."""
    channels = get_channel_status()
    latest = max(
        (dt['updated'] for dt in channels.values() if dt['updated']),
        default=None
    )

    return render_template('dashboard.html',
                         channels=channels,
                         latest=latest,
                         latest_display=format_time_ago(latest))


@app.route('/api/status')
def api_status():
    """Endpoint JSON per lo stato dei canali."""
    channels = get_channel_status()
    latest = max(
        (dt['updated'] for dt in channels.values() if dt['updated']),
        default=None
    )

    return jsonify({
        'channels': channels,
        'latest': latest,
        'latest_display': format_time_ago(latest)
    })


@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    """Esegue il refresh dei token Dailymotion."""
    try:
        result = subprocess.run(
            ['python3', 'scripts/refresh_dailymotion.py'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            # Refresh riuscito, fai git commit
            try:
                subprocess.run(['git', 'add', 'streams/'], check=True, capture_output=True)
                subprocess.run(
                    ['git', 'commit', '-m', 'Aggiorna token stream Dailymotion'],
                    check=True,
                    capture_output=True
                )
                subprocess.run(['git', 'push'], check=True, capture_output=True)
                push_status = 'success'
            except subprocess.CalledProcessError:
                # Se git fallisce, non è critico - i token sono comunque aggiornati
                push_status = 'failed'

            channels = get_channel_status()
            return jsonify({
                'status': 'success',
                'message': 'Token aggiornati con successo',
                'channels': channels,
                'git_push': push_status
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Errore nel refresh: {result.stderr}',
                'details': result.stderr
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Timeout: il refresh ha impiegato troppo tempo'
        }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Errore inatteso: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🚀 Web server avviato")
    print("📱 Accedi a: http://localhost:5000")
    print("💡 Premi Ctrl+C per fermare")
    app.run(host='127.0.0.1', port=5000, debug=False)
