import pandas as pd
import random
import os

productos_stock = {
    "Cable de Red Cat6 3m": {"min": 50, "max": 150},
    "Pasta Térmica Arctic": {"min": 20, "max": 80},
    "Memoria USB 64GB": {"min": 30, "max": 100},
    "Memoria RAM 16GB DDR4": {"min": 15, "max": 50},
    "Disco Duro SSD 1TB": {"min": 10, "max": 40},
    "Monitor 24 Pulgadas": {"min": 5, "max": 25},
    "Tarjeta Gráfica RTX 4060": {"min": 3, "max": 15},
    "Laptop Gaming Asus": {"min": 2, "max": 10},
    "Laptop Dell Inspiron": {"min": 5, "max": 20},
    "Procesador Ryzen 5": {"min": 5, "max": 25}
}

ruta_salida = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "ArchivosCSV"
)

def generar_stock():
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    ruta_completa = os.path.join(ruta_salida, "stock_actual.csv")
    ruta_historico = os.path.join(ruta_salida, "historico_maestro.csv")

    use_fallback = True
    df_hist = None
    total_dias = 1

    if os.path.exists(ruta_historico):
        try:
            df_hist = pd.read_csv(ruta_historico)
            if "Fecha" in df_hist.columns and "Producto" in df_hist.columns and "Ventas" in df_hist.columns:
                total_dias = df_hist["Fecha"].nunique()
                if total_dias == 0:
                    total_dias = 1
                use_fallback = False
        except Exception as e:
            print(f"[Warning] Error leyendo historico_maestro.csv: {e}. Usando fallback.")

    registros = []
    for producto, params in productos_stock.items():
        if not use_fallback and df_hist is not None:
            total_ventas = df_hist[df_hist["Producto"] == producto]["Ventas"].sum()
            vpd = total_ventas / total_dias
            stock_base = (vpd * 15) + max(3, vpd * 5)
            # Aplicar fluctuación aleatoria controlada de +/- 15%
            stock = int(round(stock_base * random.uniform(0.85, 1.15)))
            stock = max(3, stock)  # Garantizar al menos 3 unidades de stock inicial
        else:
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