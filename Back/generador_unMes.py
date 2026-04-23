import pandas as pd
import numpy as np

# Definimos el periodo: últimos 30 días hasta hoy
fechas = pd.date_range(start="2026-03-15", end="2026-04-13")

# Mismos productos exactos que el historico_maestro.csv para evitar errores de llave
productos = [
    "Laptop Dell Inspiron", 
    "Procesador Ryzen 5", 
    "Memoria RAM 16GB", 
    "Tarjeta Gráfica RTX 4060",
    "Monitor 24 pulgadas"
]

registros_mes = []

for producto in productos:
    # Mantenemos la misma proporción de ventas base
    if producto == "Memoria RAM 16GB":
        venta_base = 15
    elif producto == "Procesador Ryzen 5":
        venta_base = 8
    elif producto == "Monitor 24 pulgadas":
        venta_base = 6
    elif producto == "Laptop Dell Inspiron":
        venta_base = 4
    elif producto == "Tarjeta Gráfica RTX 4060":
        venta_base = 2

    for fecha in fechas:
        # Ruido aleatorio diario
        venta_del_dia = venta_base + np.random.randint(-2, 4)
        
        # Efecto Fin de Semana
        if fecha.weekday() in [4, 5]: 
            venta_del_dia += 3
            
        # Evitar números negativos
        venta_del_dia = max(0, venta_del_dia)
        
        registros_mes.append({
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Producto": producto,
            "Cantidad": venta_del_dia
        })

df_mes = pd.DataFrame(registros_mes)

# Mezclamos filas para simular el desorden de un reporte transaccional real
df_mes = df_mes.sample(frac=1).reset_index(drop=True)

# Exportamos el archivo que el usuario subirá en el Dashboard
nombre_archivo = "ventas_mes_actual.csv"
df_mes.to_csv(nombre_archivo, index=False)

print(f"¡Éxito! Archivo '{nombre_archivo}' generado correctamente.")
print(f"Total de registros: {len(df_mes)} (30 días de los 5 productos)")
print("\nPrimeras 5 filas:")
print(df_mes.head())