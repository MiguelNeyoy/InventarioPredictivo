import pandas as pd
from prophet import Prophet

class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Carga el histórico maestro y genera pronósticos para periodos específicos.
    """

    def __init__(self):
        print("Iniciando Motor de IA para Inventario...")
        # Cargar datos históricos
        self.df_historico = pd.read_csv('historico_maestro.csv')
        self.df_historico['Ventas'] = self.df_historico['Cantidad']  # Renombrar para consistencia
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

    def generar_prediccion(self, start_date, end_date):
        """
        Genera pronóstico para un periodo específico usando los datos históricos.
        """
        print(f"Generando pronóstico desde {start_date} hasta {end_date}...")
        resultados = []
        lista_productos = self.df_historico['Producto'].unique()
        
        for articulo in lista_productos:
            df_filtrado = self.df_historico[self.df_historico['Producto'] == articulo].copy()
            df_filtrado['ds'] = pd.to_datetime(df_filtrado['Fecha'])
            df_filtrado['y'] = df_filtrado['Ventas']
            
            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_filtrado[['ds', 'y']])
            
            futuro = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date, freq='D')})
            prediccion = modelo.predict(futuro)
            
            total_estimado = prediccion['yhat'].sum()
            
            resultados.append({
                "Producto": articulo,
                "Venta_Estimada": round(max(0, total_estimado)) # max(0) evita ventas negativas
            })
            
        return pd.DataFrame(resultados)