import pandas as pd

class LogicaNegocio:
    """
    Contiene las reglas de negocio sobre alertas de inventario.
    """

    def evaluar_stock(self, df_predicciones, stock_actual_dict):
        """
        Motor de reglas de negocio para emitir alertas.
        df_predicciones: DataFrame con ["Producto", "Venta_Estimada"]
        stock_actual_dict: Diccionario en forma de {"Producto": CantidadReal}
        """
        print("Evaluando inventario contra predicciones (Logica de Negocio)...")
        alertas = []
        
        # Recorremos la tabla de predicciones que genero el motor
        for index, fila in df_predicciones.iterrows():
            articulo = fila['Producto']
            estimado = fila['Venta_Estimada']
            
            # Buscamos cuánto stock tenemos en la vida real de este artículo
            # Si no nos pasan el dato, asumimos 0
            stock_real = stock_actual_dict.get(articulo, 0)
            
            # LA LÓGICA DE NEGOCIO ORIGINAL
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
