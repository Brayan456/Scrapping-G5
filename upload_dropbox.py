import os
import requests

# Variables de entorno (guárdalas como secretos en GitHub o .env local)
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

# Paso 1: obtener nuevo access_token
print("[*] Solicitando nuevo access_token...")
auth_response = requests.post(
    "https://api.dropboxapi.com/oauth2/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": DROPBOX_REFRESH_TOKEN,
    },
    auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET),
)

if auth_response.status_code != 200:
    print("[✗] Error al obtener access_token:", auth_response.text)
    exit(1)

access_token = auth_response.json()["access_token"]
print("[✓] access_token obtenido")

# Paso 2: preparar cabecera para subir archivos
headers = {
    "Authorization": f"Bearer {access_token}",
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
            "https://content.dropboxapi.com/2/files/upload",
            headers={**headers, "Dropbox-API-Arg": str({
                "path": dropbox_path,
                "mode": "overwrite",
                "autorename": False,
                "mute": False
            }).replace("'", '"')},
            data=f
        )
        if response.status_code == 200:
            print(f"[✓] Subido: {dropbox_path}")
        else:
            print(f"[✗] Error subiendo {dropbox_path}: {response.text}")
