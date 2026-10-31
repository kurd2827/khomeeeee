import os
import urllib.request
import zipfile

print("Downloading Xray Core...")
# دانلود نسخه لینوکس Xray
url = "https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip"
urllib.request.urlretrieve(url, "xray.zip")

print("Extracting files...")
with zipfile.ZipFile("xray.zip", 'r') as zip_ref:
    zip_ref.extractall(".")

# دادن دسترسی اجرا به فایل Xray
os.chmod("xray", 0o755)

print("Creating config.json...")
config_json = """
{
  "log": {"loglevel": "warning"},
  "inbounds": [
    {
      "port": 8000,
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
"""
with open("config.json", "w") as f:
    f.write(config_json)

print("Starting VLESS Proxy...")
# اجرای Xray
os.system("./xray -config config.json")