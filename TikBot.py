import sys
import time
import webbrowser
import threading
from flask import Flask, request, jsonify

# Pfad-Fix für Pydroid 3 (Wichtig für Handy-Nutzer)
sys.path.append('/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages')

try:
    from flask import Flask
except ImportError:
    print("Bitte installiere Flask im Terminal: pip install flask")
    sys.exit()

app = Flask(__name__)

# Hier wird der Status gespeichert
bot_data = {
    "current_views": 0, 
    "is_running": False,
    "target": 1000
}

# Die Logik, die die Tabs im Browser öffnet
def tab_logic(url):
    bot_data["is_running"] = True
    bot_data["current_views"] = 0
    interval = 5 # Alle 5 Sekunden ein neuer Tab/Refresh
    
    print(f"🚀 Tab-Booster gestartet für: {url}")
    
    for i in range(1, bot_data["target"] + 1):
        # Öffnet den TikTok Link im Standard-Browser
        webbrowser.open(url)
        bot_data["current_views"] = i
        
        # Konsolen-Ausgabe alle 10 Views
        if i % 10 == 0:
            print(f"📈 Fortschritt: {i} Views erreicht.")
        
        time.sleep(interval)
        
    bot_data["is_running"] = False
    print("✅ Ziel von 1000 Views erreicht.")

# Route 1: Lädt deine goldene index.html
@app.route('/')
def index():
    try:
        return open('index.html', 'r', encoding='utf-8').read()
    except FileNotFoundError:
        return "Fehler: index.html wurde im Ordner nicht gefunden!"

# Route 2: Wird aufgerufen, wenn du auf START BOOST klickst
@app.route('/api/boost', methods=['POST'])
def boost():
    data = request.json
    url = data.get('video_url')
    
    if url and not bot_data["is_running"]:
        # Startet den Bot in einem extra Thread, damit die Website nicht stehen bleibt
        threading.Thread(target=tab_logic, args=(url,)).start()
        return jsonify({"status": "started"}), 200
    
    return jsonify({"status": "error", "message": "Bot läuft bereits oder Link fehlt"}), 400

# Route 3: Liefert der Website die Zahlen in 10er Schritten (10, 20, 30...)
@app.route('/api/stats')
def get_stats():
    # Berechnet den Fortschritt (abgerundet auf die nächste 10)
    stepped_views = (bot_data["current_views"] // 10) * 10
    return jsonify({
        "views": stepped_views,
        "is_running": bot_data["is_running"]
    })

if __name__ == '__main__':
    print("\n" + "="*30)
    print("🔥 TBBF TIKBOT SYSTEM GESTARTET")
    print("👉 Öffne im Browser: http://127.0.0.1:5000")
    print("="*30 + "\n")
    
    # Startet den Webserver
    app.run(host='0.0.0.0', port=5000)

