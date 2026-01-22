import sys
import time
import webbrowser
import threading
from flask import Flask, request, jsonify

# Pfad-Fix für Pydroid 3
sys.path.append('/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages')

try:
    from flask import Flask
except:
    print("Bitte installiere Flask: pip install flask")
    sys.exit()

app = Flask(__name__)

# Status-Speicher
bot_data = {"current_views": 0, "is_running": False}

def tab_logic(url):
    bot_data["is_running"] = True
    bot_data["current_views"] = 0
    target = 1000
    interval = 5 # Sekunden pro View
    
    for i in range(1, target + 1):
        webbrowser.open(url)
        bot_data["current_views"] = i
        
        # Konsolen-Ausgang zur Kontrolle
        if i % 10 == 0:
            print(f"📈 Meilenstein: {i} Views erreicht.")
        
        time.sleep(interval)
    bot_data["is_running"] = False

@app.route('/')
def index():
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/api/boost', methods=['POST'])
def boost():
    data = request.json
    url = data.get('video_url')
    if url and not bot_data["is_running"]:
        threading.Thread(target=tab_logic, args=(url,)).start()
        return jsonify({"status": "started"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/api/stats')
def get_stats():
    # Berechnet den Fortschritt in 10er Schritten (10, 20, 30...)
    stepped_views = (bot_data["current_views"] // 10) * 10
    return jsonify({"views": stepped_views})

if __name__ == '__main__':
    print("🚀 Server läuft auf http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)

