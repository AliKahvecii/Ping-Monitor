from flask import Flask, jsonify, render_template
import subprocess
import threading
import platform
import time

def ping(ip):
    try:
        system = platform.system().lower()
        command = ["ping", "-c", "3", ip] if system != "windows" else ["ping", "-n", "1", ip]
        output = subprocess.run(command, capture_output=True, text=True, timeout=2)
        return output.returncode == 0
    except Exception:
        return False

app = Flask(__name__)

# Monitor IPs from 192.168.2.1 to 192.168.2.100
ips = [f"192.168.2.{i}" for i in range(1, 150)]
status = {ip: False for ip in ips}

def update_status():
    global status
    while True:
        for ip in ips:
            status[ip] = ping(ip)
        time.sleep(5)  # Ping every 5 seconds

threading.Thread(target=update_status, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def get_status():
    return jsonify(status)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 
