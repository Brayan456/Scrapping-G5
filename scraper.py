import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Crear carpeta con la fecha actual para organizar los datos descargados
hoy = datetime.today().strftime('%Y-%m-%d')
base_path = os.path.join("data", hoy)
os.makedirs(base_path, exist_ok=True)

# -------------------------------------
# 1. Scraping FED Funds Rate desde FRED
# -------------------------------------

# URL de la página de la FED y del CSV con los datos
fed_url = "https://fred.stlouisfed.org/series/FEDFUNDS"
fed_api_csv = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS"

try:
    # Solicitud HTTP para obtener el CSV de tasas FED
    r = requests.get(fed_api_csv)
    r.raise_for_status()  # Lanza excepción si hubo error en la descarga

    # Crear carpeta donde se almacenarán los datos de la FED
    fed_path = os.path.join("data", "fed", hoy)
    os.makedirs(fed_path, exist_ok=True)

    # Guardar el contenido descargado en un archivo CSV
    with open(os.path.join(fed_path, "fedfunds.csv"), "wb") as f:
        f.write(r.content)
    
    # Confirmación en consola
    print(f"[✓] Datos de la FED guardados en {fed_path}\\fedfunds.csv")
except Exception as e:
    # Manejo de errores en caso de fallo en la descarga
    print(f"[✗] Error al acceder a FRED: {e}")

# -------------------------------------
# 2. Scraping de inflación Perú desde TradingEconomics
# -------------------------------------


# URL de la página de ejemplo: Inflación en Perú
te_url = "https://tradingeconomics.com/peru/inflation-cpi"
categoria = "inflacion_peru"

try:
    # Realizar solicitud GET con headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    r = requests.get(te_url, headers=headers)
    r.raise_for_status()

    # Leer todas las tablas HTML de la página
    tables = pd.read_html(r.text)

    # Crear carpeta específica para esta categoría
    te_path = os.path.join("data", categoria, hoy)
    os.makedirs(te_path, exist_ok=True)

    # Guardar todas las tablas como CSV
    for i, tabla in enumerate(tables):
        archivo_csv = os.path.join(te_path, f"tabla_{i+1}.csv")
        tabla.to_csv(archivo_csv, index=False)
        print(f"[✓] Tabla {i+1} guardada en: {archivo_csv}")

except Exception as e:
    print(f"[✗] Error al acceder a TradingEconomics: {e}")

