import pandas as pd
import numpy as np

print("Generando archivo de inventario físico (stock actual)...")

# Los productos DEBEN ser exactamente los mismos para evitar fallos de cruce
productos = [
    "Laptop Dell Inspiron", 
    "Procesador Ryzen 5", 
    "Memoria RAM 16GB", 
    "Tarjeta Gráfica RTX 4060",
    "Monitor 24 pulgadas"
]

datos_stock = []

for producto in productos:
    # Asignamos inventarios realistas. Es normal tener muchas RAM y pocas Gráficas.
    if producto == "Memoria RAM 16GB":
        stock = np.random.randint(50, 150)
    elif producto == "Laptop Dell Inspiron":
        stock = np.random.randint(10, 40)
    elif producto == "Procesador Ryzen 5":
        stock = np.random.randint(20, 60)
    elif producto == "Monitor 24 pulgadas":
        stock = np.random.randint(15, 45)
    elif producto == "Tarjeta Gráfica RTX 4060":
        stock = np.random.randint(2, 12)
        
    datos_stock.append({
        "Producto": producto,
        "Stock_Actual": stock
    })

# Convertimos a DataFrame
df_stock = pd.DataFrame(datos_stock)

# Exportamos a CSV
nombre_archivo = "stock_actual.csv"
df_stock.to_csv(nombre_archivo, index=False)

print(f"¡Éxito! Archivo '{nombre_archivo}' generado correctamente.")
print("\nContenido del inventario:")
print(df_stock)