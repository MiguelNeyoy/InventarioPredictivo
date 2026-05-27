import pandas as pd
import numpy as np
from datetime import datetime
import os

productos = {
    "Cable de Red Cat6 3m": {"lam": 1.5},
    "Pasta Térmica Arctic": {"lam": 1.4},
    "Memoria USB 64GB": {"lam": 1.2},
    "Memoria RAM 16GB DDR4": {"lam": 0.0020},
    "Disco Duro SSD 1TB": {"lam": 0.0030},
    "Monitor 24 Pulgadas": {"lam": 0.0010},
    "Tarjeta Gráfica RTX 4060": {"lam": 0.0015},
    "Laptop Gaming Asus": {"lam": 0.0015},
    "Laptop Dell Inspiron": {"lam": 0.0020},
    "Procesador Ryzen 5": {"lam": 0.0030}
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

    # 1. Estacionalidad por día de la semana (Viernes=4, Sábado=5, Domingo=6 -> +35%)
    if fecha.weekday() in [4, 5, 6]:
        lam *= 1.35

    # 2. Tendencia de crecimiento anual (+8% acumulado por año a partir del base 2024)
    años_transcurridos = max(0, fecha.year - 2024)
    lam *= (1.08 ** años_transcurridos)

    # 3. Quincenas
    if fecha.day in [15, 16, 30, 31]:
        lam *= 1.5

    # 4. Temporada navideña (noviembre y diciembre)
    if fecha.month in [11, 12]:
        if lam >= 2:
            lam *= 1.5
        else:
            lam *= 1.25

    return lam

def generar_ventas_mes():
    nombre_archivo = obtener_nombre_archivo()
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)
    ruta_stock = os.path.join(ruta_salida, "stock_actual.csv")

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # Cargar niveles de stock iniciales
    stock_disponible = {}
    if os.path.exists(ruta_stock):
        try:
            df_stock = pd.read_csv(ruta_stock)
            # Manejar columnas Stock o Stock_Actual
            col_stock = "Stock_Actual" if "Stock_Actual" in df_stock.columns else ("Stock" if "Stock" in df_stock.columns else None)
            if col_stock and "Producto" in df_stock.columns:
                stock_disponible = dict(zip(df_stock["Producto"], df_stock[col_stock]))
        except Exception as e:
            print(f"[Warning] Error cargando stock_actual.csv: {e}.")
            
    # Inicializar productos faltantes en stock
    for prod in productos.keys():
        if prod not in stock_disponible:
            stock_disponible[prod] = 50

    # Guardar copia para reabastecimiento semanal
    stock_inicial = stock_disponible.copy()

    now = datetime.now()
    dias_mes = pd.date_range(start=now.replace(day=1), periods=now.day, freq="D")

    registros = []
    day_counter = 0

    for fecha in dias_mes:
        day_counter += 1
        
        # Cada 7 días se realiza un reabastecimiento (Restock) al nivel de stock inicial
        if day_counter > 1 and day_counter % 7 == 0:
            stock_disponible = stock_inicial.copy()

        for nombre_prod, params in productos.items():
            lam_ajustado = obtener_lambda_ajustado(nombre_prod, params, fecha)
            venta_dia = np.random.poisson(lam_ajustado)

            if venta_dia > 0:
                stock_actual = stock_disponible.get(nombre_prod, 0)
                
                # Simular quiebre de stock (stockout) si la demanda supera las existencias
                if venta_dia > stock_actual:
                    venta_dia = stock_actual
                    stock_disponible[nombre_prod] = 0
                else:
                    stock_disponible[nombre_prod] = stock_actual - venta_dia

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