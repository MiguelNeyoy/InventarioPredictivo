import pandas as pd
import numpy as np

print("Iniciando la simulación de datos de ventas de tecnología (3 años)...")

# Definimos el periodo de tiempo: 3 años de historia hasta hoy (Abril 2023 - Abril 2026)
fechas = pd.date_range(start="2023-04-01", end="2026-04-12")

# Elegimos productos reales de hardware/cómputo
productos = [
    "Laptop Dell Inspiron", 
    "Procesador Ryzen 5", 
    "Memoria RAM 16GB", 
    "Tarjeta Gráfica RTX 4060",
    "Monitor 24 pulgadas"
]

registros_ventas = []

for producto in productos:
    
    # Volumen realista: se venden más memorias RAM que tarjetas gráficas
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
        # A) Ruido aleatorio (variación diaria normal)
        venta_del_dia = venta_base + np.random.randint(-2, 4)
        
        # B) Efecto Fin de Semana (Viernes y Sábado hay un ligero aumento en retail)
        if fecha.weekday() in [4, 5]: 
            venta_del_dia += 3
            
        # C) Efecto Regreso a Clases (Agosto 15 - Septiembre 5)
        # Impacta muchísimo más a Laptops y Monitores
        if (fecha.month == 8 and fecha.day >= 15) or (fecha.month == 9 and fecha.day <= 5):
            if "Laptop" in producto or "Monitor" in producto:
                venta_del_dia += 12
            else:
                venta_del_dia += 3
            
        # D) Efecto Buen Fin / Black Friday (Segunda quincena de Noviembre)
        # Explosión de ventas en componentes caros (Procesadores, Gráficas)
        if fecha.month == 11 and 15 <= fecha.day <= 30:
            venta_del_dia += 25
            
        # E) Efecto Navidad (Diciembre 10 al 24)
        if fecha.month == 12 and 10 <= fecha.day <= 24:
            venta_del_dia += 15
            
        # Evitar ventas negativas por el ruido
        venta_del_dia = max(0, venta_del_dia)
        
        # Guardamos la fila respetando el esquema estricto (Fecha, Producto, Cantidad)
        registros_ventas.append({
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Producto": producto,
            "Cantidad": venta_del_dia
        })

# Convertimos a DataFrame
df_maestro = pd.DataFrame(registros_ventas)

# Mezclamos las filas aleatoriamente para simular un registro transaccional real
df_maestro = df_maestro.sample(frac=1).reset_index(drop=True)

# Exportamos a CSV
nombre_archivo = "historico_maestro.csv"
df_maestro.to_csv(nombre_archivo, index=False)

print(f"¡Éxito! Archivo '{nombre_archivo}' generado correctamente.")
print(f"Total de registros simulados: {len(df_maestro)}")
print("\nPrimeras 5 filas del archivo generado:")
print(df_maestro.head())