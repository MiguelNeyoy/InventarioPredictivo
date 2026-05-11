import pandas as pd
import random
import os

productos_stock = {
    "Cable de Red Cat6 3m": {"tipo": "alta", "min": 5, "max": 20},
    "Pasta Térmica Arctic": {"tipo": "alta", "min": 3, "max": 20},
    "Memoria USB 64GB": {"tipo": "alta", "min": 3, "max": 10},
    "Memoria RAM 16GB": {"tipo": "media", "min": 5, "max": 10},
    "SSD 1TB": {"tipo": "media", "min": 2, "max": 6},
    "Monitor 24 pulgadas": {"tipo": "media", "min": 1, "max": 5},
    "Tarjeta Gráfica RTX 4060": {"tipo": "baja", "min": 1, "max": 2},
    "Laptop Gaming Asus": {"tipo": "baja", "min": 2, "max": 7},
    "Laptop Dell Inspiron": {"tipo": "baja", "min": 1, "max": 8},
    "Procesador Ryzen 5": {"tipo": "baja", "min": 2, "max": 5}
}

ruta_salida = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ArchivosCSV"
)

def generar_stock():
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    ruta_completa = os.path.join(ruta_salida, "stock_actual.csv")

    registros = []
    for producto, params in productos_stock.items():
        stock = random.randint(params["min"], params["max"])
        registros.append({
            "Producto": producto,
            "Stock_Actual": stock
        })

    df_stock = pd.DataFrame(registros)
    df_stock = df_stock.sort_values(by="Producto").reset_index(drop=True)

    df_stock.to_csv(ruta_completa, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {ruta_completa}")
    return ruta_completa

if __name__ == "__main__":
    generar_stock()