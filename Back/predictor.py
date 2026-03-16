import pandas as pd
from prophet import Prophet

class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Procesa múltiples productos, genera pronósticos y evalúa alertas de reabastecimiento.
    """

    def __init__(self):
        print("Iniciando Motor de IA para Inventario...")
        # Aquí configuramos los días festivos locales 6
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

    def limpiar_datos(self, df_crudo):
        """
            2: Recibe el Excel sucio y lo prepara para Prophet.
        """
        print("Limpiando datos y formateando columnas...")
        # Eliminar filas vacías
        df_limpio = df_crudo.dropna().copy()
        
        # Renombrar columnas a lo que Prophet exige (ds y y)
        # Asumimos que el Excel original tiene columnas 'Fecha', 'Producto', 'Ventas'
        df_limpio = df_limpio.rename(columns={
            'Fecha': 'ds', 
            'Ventas': 'y'
        })
        
        # Asegurarnos de que la columna 'ds' sea formato fecha de Pandas
        df_limpio['ds'] = pd.to_datetime(df_limpio['ds'])
        
        return df_limpio

    def generar_prediccion(self, df_limpio, dias_a_predecir):
        """
         El Bucle Mágico que predice artículo por artículo.
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

    def evaluar_stock(self, df_predicciones, stock_actual_dict):
        """
        Motor de reglas de negocio para emitir alertas.
        """
        print("Evaluando inventario contra predicciones...")
        alertas = []
        
        # Recorremos la tabla de predicciones que acabamos de generar
        for index, fila in df_predicciones.iterrows():
            articulo = fila['Producto']
            estimado = fila['Venta_Estimada']
            
            # Buscamos cuánto stock tenemos en la vida real de este artículo
            # Si no nos pasan el dato, asumimos 0
            stock_real = stock_actual_dict.get(articulo, 0)
            
            # LA LÓGICA DE NEGOCIO
            if estimado > stock_real:
                estado_alerta = True
                cantidad_a_comprar = estimado - stock_real
            else:
                estado_alerta = False
                cantidad_a_comprar = 0
                
            alertas.append({
                "Producto": articulo,
                "Venta_Estimada": estimado,
                "Stock_Actual": stock_real,
                "Cantidad_A_Comprar": cantidad_a_comprar,
                "Alerta_Surtir": estado_alerta
            })
            
        return pd.DataFrame(alertas)