import pandas as pd
from prophet import Prophet

class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Recibe un DataFrame ya validado y listo, para generar pronosticos.
    """

    def __init__(self):
        print("Iniciando Motor de IA para Inventario...")
        # Aquí configuramos los días festivos locales 
        # Esto le dirá a la IA que espere picos de venta en estas fechas
        feriados_mazatlan = pd.DataFrame({
            'holiday': 'temporada_alta_mazatlan',
            'ds': pd.to_datetime(['2026-02-15', '2026-02-16', '2026-02-17', # Carnaval
                                  '2026-03-30', '2026-03-31', '2026-04-01', # Semana Santa
                                  '2026-04-02', '2026-04-03', '2026-04-04']),
            'lower_window': -1,
            'upper_window': 1,
        })
        self.feriados = feriados_mazatlan

    def generar_prediccion(self, df_limpio, dias_a_predecir):
        """
        El Bucle Mágico que predice artículo por artículo.
        Espera que df_limpio ya tenga las columnas 'ds', 'Producto', y 'y'.
        """
        print(f"Generando pronóstico para los próximos {dias_a_predecir} días...")
        resultados = []
        lista_productos = df_limpio['Producto'].unique()
        
        for articulo in lista_productos:
           
            df_filtrado = df_limpio[df_limpio['Producto'] == articulo]
            
            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_filtrado[['ds', 'y']])
            
            futuro = modelo.make_future_dataframe(periods=dias_a_predecir, freq='D')
            prediccion = modelo.predict(futuro)
            
            total_estimado = prediccion['yhat'].tail(dias_a_predecir).sum()
            
            resultados.append({
                "Producto": articulo,
                "Venta_Estimada": round(max(0, total_estimado)) # max(0) evita ventas negativas
            })
            
        return pd.DataFrame(resultados)