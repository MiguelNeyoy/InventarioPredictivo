import pandas as pd


class LogicaNegocio:
    """
    Contiene las reglas de negocio sobre alertas de inventario.
    """

    def evaluar_stock(self, df_predicciones, stock_actual_dict, porcentaje_seguridad=0):
        """
        Motor de reglas de negocio para emitir alertas.
        df_predicciones: DataFrame con ["Producto", "Venta_Estimada"]
        stock_actual_dict: Diccionario en forma de {"Producto": CantidadReal}
        porcentaje_seguridad: Margen adicional (%) sobre el estimado (default: 0)
        """
        print("Evaluando inventario contra predicciones (Logica de Negocio)...")
        alertas = []

        for index, fila in df_predicciones.iterrows():
            articulo = fila["Producto"]
            estimado = fila["Venta_Estimada"]

            stock_real = stock_actual_dict.get(articulo, 0)

            stock_requerido = estimado * (1 + porcentaje_seguridad / 100)

            if stock_requerido > stock_real:
                estado_alerta = True
                cantidad_a_comprar = stock_requerido - stock_real
            else:
                estado_alerta = False
                cantidad_a_comprar = 0

            alertas.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": estimado,
                    "Stock_Actual": stock_real,
                    "Cantidad_A_Comprar": round(cantidad_a_comprar),
                    "Alerta_Surtir": estado_alerta,
                }
            )

        return pd.DataFrame(alertas)
    