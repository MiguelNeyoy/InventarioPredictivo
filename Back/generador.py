import pandas as pd
import numpy as np
import random

# Catálogo realista categorizado por comportamiento de venta
productos = {
    # ROTACIÓN ALTA: Se venden todos los días (Accesorios baratos)
    "Cable de Red Cat6 3m": {"tipo": "alta", "min": 3, "max": 12}, # Reemplazo de HDMI
    "Pasta Térmica Arctic": {"tipo": "alta", "min": 1, "max": 6},
    "Memoria USB 64GB": {"tipo": "alta", "min": 4, "max": 10},
    
    # ROTACIÓN MEDIA: Se venden a veces (Componentes)
    "Memoria RAM 16GB DDR4": {"tipo": "media", "probabilidad_venta": 0.6, "cantidad": [1, 2]},
    "SSD 1TB": {"tipo": "media", "probabilidad_venta": 0.5, "cantidad": [1, 2]},
    "Monitor 24 Pulgadas": {"tipo": "media", "probabilidad_venta": 0.4, "cantidad": [1]},
    
    # ROTACIÓN BAJA: Caros, se venden muy esporádicamente (Laptops, Gráficas)
    "Tarjeta Gráfica RTX 4060": {"tipo": "baja", "probabilidad_venta": 0.10}, 
    "Laptop Gaming Asus": {"tipo": "baja", "probabilidad_venta": 0.08},       
    "Laptop Dell Inspiron": {"tipo": "baja", "probabilidad_venta": 0.15},     
    "Procesador Ryzen 5": {"tipo": "baja", "probabilidad_venta": 0.20}        
}

fechas = pd.date_range(start="2024-01-01", end="2026-03-14")
registros = []

for nombre_prod, params in productos.items():
    for fecha in fechas:
        venta_dia = 0
        
        # LÓGICA DE VENTA SEGÚN EL TIPO DE PRODUCTO
        if params["tipo"] == "alta":
            # Siempre se vende algo, cantidad aleatoria
            venta_dia = random.randint(params["min"], params["max"])
            
        elif params["tipo"] == "media":
            # A veces no se vende nada en todo el día
            if random.random() <= params["probabilidad_venta"]:
                venta_dia = random.choice(params["cantidad"])
                
        elif params["tipo"] == "baja":
            # Casi nunca se vende. Si se vende, es solo 1 unidad.
            if random.random() <= params["probabilidad_venta"]:
                venta_dia = 1

        # EFECTOS ESTACIONALES (Solo aplican si hubo al menos 1 venta o forzamos tráfico)
        
        # Efecto Quincena (Días 15 y 30/31 hay dinero, sube probabilidad de Laptops)
        if fecha.day in [15, 16, 30, 31] and params["tipo"] == "baja":
            if random.random() <= 0.30: # La probabilidad sube a 30% en quincena
                venta_dia = 1

        # Efecto Buen Fin / Navidad (Nov-Dic)
        if fecha.month in [11, 12]:
            if params["tipo"] == "alta":
                venta_dia = int(venta_dia * 1.5)
            elif params["tipo"] == "baja" and random.random() <= 0.25: # Más Laptops en Navidad
                venta_dia = random.randint(1, 2)

        # Solo guardamos si se vendió algo
        if venta_dia > 0:
            registros.append({
                "Fecha": fecha.strftime("%Y-%m-%d"),
                "Producto": nombre_prod,
                "Cantidad": venta_dia
            })

df_historico = pd.DataFrame(registros)
df_historico = df_historico.sort_values(by="Fecha").reset_index(drop=True)

df_historico.to_csv("historico_maestro.csv", index=False)
