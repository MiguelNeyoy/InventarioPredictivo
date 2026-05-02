import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Recibe un DataFrame unificado y genera pronósticos para períodos específicos.
    """

    def __init__(self, df_unificado):
        self.df_historico = df_unificado
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

    def generar_prediccion(self, start_date, end_date):
        """
        Genera pronóstico para un periodo específico usando los datos históricos.
        """
        resultados = []
        lista_productos = self.df_historico["Producto"].unique()

        for articulo in lista_productos:
            df_filtrado = self.df_historico[
                self.df_historico["Producto"] == articulo
            ].copy()

            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_filtrado[["ds", "y"]])

            futuro = pd.DataFrame(
                {"ds": pd.date_range(start=start_date, end=end_date, freq="D")}
            )
            prediccion = modelo.predict(futuro)

            total_estimado = prediccion["yhat"].sum()

            resultados.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": round(
                        max(0, total_estimado)
                    ),  # max(0) evita ventas negativas
                }
            )

        return pd.DataFrame(resultados)

    def generar_prediccion_y_metricas(self, start_date, end_date, dias_test=15):
        resultados = []
        metricas = []
        lista_productos = self.df_historico["Producto"].unique()

        for articulo in lista_productos:
            df_articulo = self.df_historico[
                self.df_historico["Producto"] == articulo
            ].copy()
            df_articulo = df_articulo.sort_values("ds")

            modelo = Prophet(holidays=self.feriados)
            modelo.fit(df_articulo[["ds", "y"]])

            futuro = pd.DataFrame(
                {"ds": pd.date_range(start=start_date, end=end_date, freq="D")}
            )
            prediccion = modelo.predict(futuro)
            total_estimado = prediccion["yhat"].sum()

            resultados.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": round(max(0, total_estimado)),
                }
            )

            if dias_test >= 5 and len(df_articulo) > dias_test:
                df_entrenamiento = df_articulo.iloc[:-dias_test]
                df_test = df_articulo.iloc[-dias_test:]

                modelo_test = Prophet(holidays=self.feriados)
                modelo_test.fit(df_entrenamiento[["ds", "y"]])
                prediccion_test = modelo_test.predict(df_test[["ds"]])

                y_real = df_test["y"].values
                y_predicho = prediccion_test["yhat"].values

                mae = mean_absolute_error(y_real, y_predicho)
                rmse = np.sqrt(mean_squared_error(y_real, y_predicho))

                metricas.append(
                    {
                        "Producto": articulo,
                        "MAE": round(mae, 2),
                        "RMSE": round(rmse, 2),
                    }
                )

        return pd.DataFrame(resultados), pd.DataFrame(
            metricas, columns=["Producto", "MAE", "RMSE"]
        )

    # def calcular_metricas(self, dias_test=15):
    #     """
    #     Calcula MAE y RMSE apartando los últimos dias_test para validación.
    #     """
    #     resultados = []
    #     lista_productos = self.df_historico["Producto"].unique()

    #     for articulo in lista_productos:
    #         df_articulo = self.df_historico[
    #             self.df_historico["Producto"] == articulo
    #         ].copy()
    #         df_articulo = df_articulo.sort_values("ds")

    #         if len(df_articulo) <= dias_test:
    #             continue

    #         df_entrenamiento = df_articulo.iloc[:-dias_test]
    #         df_test = df_articulo.iloc[-dias_test:]

    #         modelo = Prophet(holidays=self.feriados)
    #         modelo.fit(df_entrenamiento[["ds", "y"]])

    #         futuro = df_test[["ds"]]
    #         prediccion = modelo.predict(futuro)

    #         y_real = df_test["y"].values
    #         y_predicho = prediccion["yhat"].values

    #         mae = mean_absolute_error(y_real, y_predicho)
    #         rmse = np.sqrt(mean_squared_error(y_real, y_predicho))

    #         resultados.append(
    #             {"Producto": articulo, "MAE": round(mae, 2), "RMSE": round(rmse, 2)}
    #         )

    #     return pd.DataFrame(resultados)
