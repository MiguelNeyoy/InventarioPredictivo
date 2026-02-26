import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt


class MotorInventario:
    
    def __init__(self):
        # Cuando tu compañero cree el objeto, esto se ejecuta primero.
        # Aquí podrías cargar los días festivos de Mazatlán en el futuro.
        print("Iniciando Motor de IA para Inventario...")
        
    def limpiar_datos(self, dataframe_crudo):
        # Tu compañero te pasa el archivo sucio, tú devuelves uno limpio
        df_limpio = dataframe_crudo.dropna() # Ejemplo: quita nulos
        df_limpio = df_limpio.rename(columns={'Fecha': 'ds', 'Ventas': 'y'})
        return df_limpio
        
    def generar_prediccion(self, df_limpio, dias_a_predecir=15):
        # Aquí metes el "Bucle Mágico" que vimos antes
        resultados = []
        lista_productos = df_limpio['Producto'].unique()
        
        for articulo in lista_productos:
            df_filtrado = df_limpio[df_limpio['Producto'] == articulo]
            
            # Entrenar IA
            modelo = Prophet()
            modelo.fit(df_filtrado[['ds', 'y']])
            
            # Predecir
            futuro = modelo.make_future_dataframe(periods=dias_a_predecir)
            prediccion = modelo.predict(futuro)
            total_estimado = prediccion['yhat'].tail(dias_a_predecir).sum()
            
            resultados.append({
                "Producto": articulo,
                "Surtir_Estimado": round(total_estimado)
            })
            
        # Devuelves un DataFrame (Tabla) directo a tu compañero
        return pd.DataFrame(resultados)