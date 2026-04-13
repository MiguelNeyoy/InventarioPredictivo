import pandas as pd


class LogicaNegocio:
    """
    Contiene las reglas de negocio sobre alertas de inventario.
    """

    def __init__(self, umbral_seguridad=0.0):
        self.umbral_seguridad = umbral_seguridad

    def evaluar_stock(self, df_predicciones, stock_actual_dict):
        """
        Motor de reglas de negocio para emitir alertas.
        df_predicciones: DataFrame con ["Producto", "Venta_Estimada"]
        stock_actual_dict: Diccionario en forma de {"Producto": CantidadReal}
        umbral_seguridad: Porcentaje extra de colchón (0.0 = sin margen, 0.15 = 15% extra)
        """
        print("Evaluando inventario contra predicciones (Logica de Negocio)...")

        if self.umbral_seguridad > 0:
            print(f"Con margen de seguridad aplicado: {self.umbral_seguridad * 100}%")

        alertas = []

        for index, fila in df_predicciones.iterrows():
            articulo = fila["Producto"]
            estimado = fila["Venta_Estimada"]

            stock_real = stock_actual_dict.get(articulo, 0)

            necesario = estimado * (1 + self.umbral_seguridad)

            if stock_real < necesario:
                estado_alerta = True
                cantidad_a_comprar = round(necesario - stock_real)
            else:
                estado_alerta = False
                cantidad_a_comprar = 0

            alertas.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": estimado,
                    "Stock_Actual": stock_real,
                    "Cantidad_A_Comprar": cantidad_a_comprar,
                    "Alerta_Surtir": estado_alerta,
                    "Colchon_Aplicado": f"{self.umbral_seguridad * 100}%",
                }
            )

        return pd.DataFrame(alertas)
