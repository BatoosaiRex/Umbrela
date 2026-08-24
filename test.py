import pandas as pd
from playwright.sync_api import sync_playwright
import time
from playwright.sync_api import TimeoutError

df = pd.read_excel(r"D:\Doc\OneDrive\Nokia\Archivo Carga.xlsx")

for idx, row in df.iterrows():
    # saltar filas vacías
    if row.isna().all():
        continue

    print(f"Procesando fila {idx + 1}")

    print(row['siteName'])
    