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

# Encabezados HTTP para simular un navegador y evitar bloqueo
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# URL de la página de inflación de Perú en TradingEconomics
te_url = "https://es.tradingeconomics.com/peru/inflation-cpi"

try:
    # Solicitud HTTP a la página de TradingEconomics
    r = requests.get(te_url, headers=headers)
    r.raise_for_status()  # Lanza excepción si hubo error

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser")

    # Buscar elementos que contengan el nombre del indicador y su valor actual
    indicador = soup.find("span", class_="pull-left")  # Esto puede requerir ajuste si cambia el HTML
    valor = soup.find("span", class_="pull-right")

    # Si ambos elementos fueron encontrados, combinarlos
    if indicador and valor:
        inflacion = indicador.get_text(strip=True) + ": " + valor.get_text(strip=True)
    else:
        inflacion = "No se pudo extraer valor correctamente."

    # Crear carpeta donde se almacenará el dato de inflación
    te_path = os.path.join("data", "tradingeconomics", hoy)
    os.makedirs(te_path, exist_ok=True)

    # Guardar el dato de inflación en un archivo de texto
    with open(os.path.join(te_path, "inflacion.txt"), "w", encoding="utf-8") as f:
        f.write(inflacion)

    # Confirmación en consola
    print(f"[✓] Inflación Perú guardada en {te_path}\\inflacion.txt")
except Exception as e:
    # Manejo de errores en caso de fallo en la descarga o parseo
    print(f"[✗] Error al acceder a tradingeconomics: {e}")
