import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Recibe un DataFrame ya validado y listo, para generar pronosticos.
    """

    def __init__(self):
        print("Iniciando Motor de IA para Inventario...")
        # Aquí configuramos los días festivos locales
        # Esto le dirá a la IA que espere picos de venta en estas fechas
        feriados_mazatlan = pd.DataFrame(
            {
                "holiday": "temporada_alta_mazatlan",
                "ds": pd.to_datetime(
                    [
                        "2026-02-15",
                        "2026-02-16",
                        "2026-02-17",  # Carnaval
                        "2026-03-30",
                        "2026-03-31",
                        "2026-04-01",  # Semana Santa
                        "2026-04-02",
                        "2026-04-03",
                        "2026-04-04",
                    ]
                ),
                "lower_window": -1,
                "upper_window": 1,
            }
        )
        self.feriados = feriados_mazatlan

    def generar_prediccion(self, df_limpio, dias_a_predecir):
        """
        El Bucle Mágico que predice artículo por artículo.
        Espera que df_limpio ya tenga las columnas 'ds', 'Producto', y 'y'.
        """
        print(f"Generando pronóstico para los próximos {dias_a_predecir} días...")
        resultados = []
        lista_productos = df_limpio["Producto"].unique()

        for articulo in lista_productos:
            df_filtrado = df_limpio[df_limpio["Producto"] == articulo]

            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_filtrado[["ds", "y"]])

            futuro = modelo.make_future_dataframe(periods=dias_a_predecir, freq="D")
            prediccion = modelo.predict(futuro)

            total_estimado = prediccion["yhat"].tail(dias_a_predecir).sum()

            resultados.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": round(
                        max(0, total_estimado)
                    ),  # max(0) evita ventas negativas
                }
            )

        return pd.DataFrame(resultados)

    def evaluar_modelo(self, df_limpio, dias_ocultos=15):
        """
        Evalúa el margen de error del modelo ocultando los últimos dias_ocultos
        dias del dataset y comparándolos con la predicción.

        Retorna un DataFrame con métricas por producto.
        """
        print(f"Evaluando modelo con {dias_ocultos} días ocultados para validación...")

        lista_productos = df_limpio["Producto"].unique()
        resultados_evaluacion = []

        for articulo in lista_productos:
            df_producto = df_limpio[df_limpio["Producto"] == articulo].copy()
            df_producto = df_producto.sort_values("ds").reset_index(drop=True)

            if len(df_producto) <= dias_ocultos:
                resultados_evaluacion.append(
                    {
                        "Producto": articulo,
                        "MAE": None,
                        "RMSE": None,
                        "Nota": f"Datos insuficientes para evaluar (total: {len(df_producto)})",
                    }
                )
                continue

            df_entrenamiento = df_producto.iloc[:-dias_ocultos]
            df_real = df_producto.iloc[-dias_ocultos:]

            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_entrenamiento[["ds", "y"]])

            futuro = modelo.make_future_dataframe(periods=dias_ocultos, freq="D")
            prediccion = modelo.predict(futuro)

            valores_predichos = prediccion["yhat"].tail(dias_ocultos).values
            valores_reales = df_real["y"].values

            mae = mean_absolute_error(valores_reales, valores_predichos)
            rmse = np.sqrt(mean_squared_error(valores_reales, valores_predichos))

            resultados_evaluacion.append(
                {
                    "Producto": articulo,
                    "MAE": round(mae, 2),
                    "RMSE": round(rmse, 2),
                    "Nota": "Evaluación completada",
                }
            )

        return pd.DataFrame(resultados_evaluacion)
