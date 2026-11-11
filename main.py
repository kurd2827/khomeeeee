import os
import urllib.request
import zipfile
import json
import threading
import subprocess
from flask import Flask, request, Response
import requests

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))
XRAY_PORT = 10000

print("Downloading Xray Core (musl compatible)...")
# حتما از نسخه alpine (musl) استفاده می‌کنیم تا در هر محیط لینوکسی سبک اجرا شود
url = "https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip"
urllib.request.urlretrieve(url, "xray.zip")

print("Extracting files...")
with zipfile.ZipFile("xray.zip", 'r') as zip_ref:
    zip_ref.extractall(".")

print("Setting execute permissions...")
os.chmod("xray", 0o755)

print("Creating config.json...")
config_json = {
    "log": {"loglevel": "warning"},
    "inbounds": [
        {
            "port": XRAY_PORT,
            "listen": "127.0.0.1", # فقط به صورت محلی گوش می‌دهد تا کرش نکند
            "protocol": "vless",
            "settings": {
                "clients": [{"id": "d3b80890-3498-44fb-a589-73b37803e7c8", "level": 0}],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {"path": "/mardinkurd"}
            }
        }
    ],
    "outbounds": [{"protocol": "freedom"}]
}

with open("config.json", "w") as f:
    json.dump(config_json, f, indent=2)

def run_xray():
    print("Starting Xray Proxy Process...")
    # اجرای بدون بافر تا لاگ‌ها دیده شود
    subprocess.Popen(["./xray", "-config", "config.json"])

# اجرای Xray در بک‌گراند
threading.Thread(target=run_xray, daemon=True).start()

# مسیر اصلی برای سبز شدن Health Check پنل
@app.route('/')
def health_check():
    return "Xray Proxy Server is Active!", 200

# هدایت تمام ترافیک وب‌سوکت به پورت Xray
@app.route('/mardinkurd', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy():
    url = f"http://127.0.0.1:{XRAY_PORT}/mardinkurd"
    # انتقال ترافیک
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Proxy Error: {e}", 502

if __name__ == '__main__':
    print(f"Flask Web Server listening on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT)
