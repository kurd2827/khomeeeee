import os
import urllib.request
import zipfile
import json
import subprocess

print("Downloading Xray Core...")
# دانلود نسخه لینوکس
url = "https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip"
urllib.request.urlretrieve(url, "xray.zip")

print("Extracting files...")
with zipfile.ZipFile("xray.zip", 'r') as zip_ref:
    zip_ref.extractall(".")

# دادن دسترسی اجرا به فایل
os.chmod("xray", 0o755)

print("Creating config.json...")
# دریافت پورت از سرور ابری، اگر نبود 8080 در نظر بگیر
server_port = int(os.environ.get("PORT", 8080))

config_json = {
    "log": {"loglevel": "warning"},
    "inbounds": [
        {
            "port": server_port,
            "listen": "0.0.0.0",
            "protocol": "vless",
            "settings": {
                "clients": [
                    {
                        "id": "d3b80890-3498-44fb-a589-73b37803e7c8",
                        "level": 0
                    }
                ],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {
                    "path": "/mardinkurd"
                }
            }
        }
    ],
    "outbounds": [{"protocol": "freedom"}]
}

with open("config.json", "w") as f:
    json.dump(config_json, f, indent=4)

print(f"Starting VLESS Proxy on port {server_port}...")

# استفاده از subprocess.run به جای os.system تا کانتینر بسته نشود
try:
    subprocess.run(["./xray", "-config", "config.json"], check=True)
except Exception as e:
    print(f"Failed to run Xray: {e}")
