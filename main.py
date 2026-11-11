import os
import urllib.request
import zipfile
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

print("Downloading Xray Core...")
# لینک مستقیم برای نسخه سازگار با لینوکس
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
            "port": 8000,
            "listen": "0
