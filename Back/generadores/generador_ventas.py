import pandas as pd
import numpy as np
from datetime import datetime
import os

productos = {
    "Cable de Red Cat6 3m": {"lam": 1.5},
    "Pasta Térmica Arctic": {"lam": 1.5},
    "Memoria USB 64GB": {"lam": 0.9},
    "Memoria RAM 16GB DDR4": {"lam": 0.20},
    "Disco Duro SSD 1TB": {"lam": 0.3},
    "Monitor 24 Pulgadas": {"lam": 0.1},
    "Tarjeta Gráfica RTX 4060": {"lam": 0.15},
    "Laptop Gaming Asus": {"lam": 0.155},
    "Laptop Dell Inspiron": {"lam": 0.2},
    "Procesador Ryzen 5": {"lam": 0.3}
}

ruta_salida = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "ArchivosCSV"
)

def obtener_mes_actual():
    meses = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    now = datetime.now()
    return meses[now.month], now.year

def obtener_nombre_archivo():
    mes, año = obtener_mes_actual()
    return f"ventas_{mes}_{año}.csv"

def obtener_lambda_ajustado(producto, params, fecha):
    lam = params["lam"]

    if fecha.day in [15, 16, 30, 31]:
        lam *= 1.5

    if fecha.month in [11, 12]:
        if lam >= 2:
            lam *= 1.5
        else:
            lam *= 1.25

    return lam

def generar_ventas_mes():
    nombre_archivo = obtener_nombre_archivo()
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    now = datetime.now()
    dias_mes = pd.date_range(start=now.replace(day=1), periods=now.day, freq="D")

    registros = []
    for fecha in dias_mes:
        for nombre_prod, params in productos.items():
            lam_ajustado = obtener_lambda_ajustado(nombre_prod, params, fecha)
            venta_dia = np.random.poisson(lam_ajustado)

            if venta_dia > 0:
                registros.append({
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "Producto": nombre_prod,
                    "Ventas": int(venta_dia)
                })

    df_ventas = pd.DataFrame(registros)
    df_ventas = df_ventas.sort_values(by="Fecha").reset_index(drop=True)

    df_ventas.to_csv(ruta_completa, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {ruta_completa}")
    return ruta_completa

if __name__ == "__main__":
    generar_ventas_mes()