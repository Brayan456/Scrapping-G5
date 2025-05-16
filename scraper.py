import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Crear carpeta por fecha
hoy = datetime.today().strftime('%Y-%m-%d')
base_path = os.path.join("data", hoy)
os.makedirs(base_path, exist_ok=True)

# -------------------------------------
# 1. Scraping FED Funds Rate desde FRED
# -------------------------------------

fed_url = "https://fred.stlouisfed.org/series/FEDFUNDS"
fed_api_csv = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS"

try:
    r = requests.get(fed_api_csv)
    r.raise_for_status()
    fed_path = os.path.join("data", "fed", hoy)
    os.makedirs(fed_path, exist_ok=True)
    with open(os.path.join(fed_path, "fedfunds.csv"), "wb") as f:
        f.write(r.content)
    print(f"[✓] Datos de la FED guardados en {fed_path}\\fedfunds.csv")
except Exception as e:
    print(f"[✗] Error al acceder a FRED: {e}")

# -------------------------------------
# 2. Scraping de inflación Perú desde TradingEconomics
# -------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

te_url = "https://es.tradingeconomics.com/peru/inflation-cpi"

try:
    r = requests.get(te_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")

    # Buscar el valor de inflación actual (esto depende del HTML de la página)
    indicador = soup.find("span", class_="pull-left")  # puede que necesites adaptar esto
    valor = soup.find("span", class_="pull-right")

    if indicador and valor:
        inflacion = indicador.get_text(strip=True) + ": " + valor.get_text(strip=True)
    else:
        inflacion = "No se pudo extraer valor correctamente."

    te_path = os.path.join("data", "tradingeconomics", hoy)
    os.makedirs(te_path, exist_ok=True)
    with open(os.path.join(te_path, "inflacion.txt"), "w", encoding="utf-8") as f:
        f.write(inflacion)

    print(f"[✓] Inflación Perú guardada en {te_path}\\inflacion.txt")
except Exception as e:
    print(f"[✗] Error al acceder a tradingeconomics: {e}")
