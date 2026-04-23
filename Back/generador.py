import pandas as pd
import numpy as np

#  Definimos el periodo de tiempo (2 años de historia hasta el día de hoy)
fechas = pd.date_range(start="2024-01-01", end="2026-02-27")

# Elegimos productos realistas para la costa
productos = ["Cerveza Pacifico", "Bloqueador Solar", "Hielo en Bolsa"]

# Aquí guardaremos todos los registros antes de hacer el Excel
registros_ventas = []

# Simulamos las ventas día por día, producto por producto
for producto in productos:
    
    # Cada producto tiene una venta base diferente
    if producto == "Cerveza Pacifico":
        venta_base = 80
    elif producto == "Bloqueador Solar":
        venta_base = 30
    else:
        venta_base = 50

    for fecha in fechas:
        # A) Añadimos ruido aleatorio (las ventas nunca son exactamente iguales)
        venta_del_dia = venta_base + np.random.randint(-15, 20)
        
        # B) Efecto Fin de Semana (Viernes, Sábado y Domingo se vende más)
        if fecha.weekday() >= 4: # 4 es Viernes, 5 Sábado, 6 Domingo
            venta_del_dia += 40
            
        # C) Efecto Carnaval (Picos masivos a finales de febrero)
        if fecha.month == 2 and 15 <= fecha.day <= 25:
            venta_del_dia += 120
            
        # D) Efecto Semana Santa (Picos masivos en abril)
        if fecha.month == 4 and 1 <= fecha.day <= 15:
            venta_del_dia += 150
            
        # Asegurarnos de que no existan ventas negativas por el ruido aleatorio
        venta_del_dia = max(0, venta_del_dia)
        
        # Guardamos la fila
        registros_ventas.append({
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Producto": producto,
            "Ventas": venta_del_dia
        })

#  Convertimos la lista en una tabla (DataFrame)
df_maestro = pd.DataFrame(registros_ventas)

#  EL TOQUE DE REALIDAD: Mezclamos las filas aleatoriamente
# Esto simula un registro real donde la gente compra a distintas horas
df_maestro = df_maestro.sample(frac=1).reset_index(drop=True)

#  Exportamos a CSV
df_maestro.to_csv("ventas_totales.csv", index=False)

print("¡Éxito! Archivo 'ventas_totales.csv' generado correctamente.")
print(f"Total de registros simulados: {len(df_maestro)}")
print("\nPrimeras 5 filas del archivo revuelto:")
print(df_maestro.head())