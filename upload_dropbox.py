import os
import requests

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_API = "https://content.dropboxapi.com/2/files/upload"

headers = {
    "Authorization": f"Bearer {DROPBOX_TOKEN}",
    "Content-Type": "application/octet-stream",
}

files_to_upload = [
    ("data/fed/2025-05-16/fedfunds.csv", "/fedfunds.csv"),
    ("data/tradingeconomics/2025-05-16/inflacion.txt", "/inflacion.txt")
]

for local_path, dropbox_path in files_to_upload:
    if not os.path.exists(local_path):
        print(f"[!] No existe: {local_path}")
        continue

    with open(local_path, "rb") as f:
        print(f"[+] Subiendo {local_path} a Dropbox en {dropbox_path}")
        response = requests.post(
            DROPBOX_API,
            headers={**headers, "Dropbox-API-Arg": str({"path": dropbox_path, "mode": "overwrite", "autorename": False, "mute": False}).replace("'", '"')},
            data=f
        )
        if response.status_code == 200:
            print(f"[✓] Subido: {dropbox_path}")
        else:
            print(f"[✗] Error subiendo {dropbox_path}: {response.text}")
