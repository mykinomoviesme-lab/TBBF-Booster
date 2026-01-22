import os
import threading
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Globaler Speicher für den Status des Bots
bot_status = {
    "views_done": 0,
    "target": 0,
    "is_running": False,
    "stop_signal": False
}

def boost_logic(url, target, duration):
    global bot_status
    bot_status["is_running"] = True
    bot_status["stop_signal"] = False
    bot_status["views_done"] = 0
    bot_status["target"] = target

    # Video-ID aus dem Link extrahieren
    try:
        if "/video/" in url:
            video_id = url.split("/video/")[1].split("?")[0]
        else:
            # Falls Kurz-URL, Link auflösen
            r = requests.get(url, allow_redirects=True, timeout=10)
            video_id = r.url.split("/video/")[1].split("?")[0]
    except Exception as e:
        print(f"Fehler bei Link-Analyse: {e}")
        bot_status["is_running"] = False
        return

    print(f"🚀 Booster gestartet für ID: {video_id} | Ziel: {target}")

    headers = {
        "User-Agent": "com.zhiliaoapp.musically/2022405040",
        "Host": "api16-core-c-useast1a.tiktokv.com"
    }
    api_url = f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/?item_id={video_id}&play_delta=1"

    for i in range(1, target + 1):
        # Prüfen, ob der User "STOPP" gedrückt hat
        if bot_status["stop_signal"]:
            print("🛑 Bot wurde manuell gestoppt.")
            break
        
        try:
            # Der eigentliche View-Befehl
            response = requests.post(api_url, headers=headers, timeout=5)
            if response.status_code == 200:
                bot_status["views_done"] = i
        except Exception as e:
            print(f"Request Fehler: {e}")
        
        # Wartezeit zwischen den Views (Eingabefeld von der Webseite)
        time.sleep(duration)

    bot_status["is_running"] = False
    print(f"✅ Vorgang beendet. Gesamtviews in dieser Sitzung: {bot_status['views_done']}")

# ROUTEN FÜR DIE WEBSITE

@app.route('/')
def index():
    # Lädt deine Index.html
    try:
        return open('Index.html', 'r', encoding='utf-8').read()
    except:
        return "Fehler: Index.html nicht gefunden!"

@app.route('/api/start', methods=['POST'])
def start():
    data = request.json
    url = data.get('url')
    target = int(data.get('target', 1000))
    duration = float(data.get('duration', 2))

    if not bot_status["is_running"]:
        # Startet den Bot in einem eigenen Thread (Hintergrund)
        threading.Thread(target=boost_logic, args=(url, target, duration)).start()
        return jsonify({"status": "started"}), 200
    return jsonify({"status": "already_running"}), 400

@app.route('/api/stop', methods=['POST'])
def stop():
    bot_status["stop_signal"] = True
    return jsonify({"status": "stopping"}), 200

@app.route('/api/stats')
def stats():
    # Berechnet die Anzeige in 10er Schritten für das Design
    display_views = (bot_status["views_done"] // 10) * 10
    return jsonify({
        "views": display_views,
        "is_running": bot_status["is_running"],
        "real_count": bot_status["views_done"]
    })

if __name__ == '__main__':
    # Port 8080 ist Standard für Replit
    app.run(host='0.0.0.0', port=8080)

