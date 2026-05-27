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
                        "2026-02-05",  #Inicio Infomatrix pacifico
                        "2026-02-06",
                        "2026-02-07",  #Fin Infomatrix pacifico
                        "2026-05-25",  #Inicio hot sale
                        "2026-05-26",
                        "2026-05-27",
                        "2026-05-28",
                        "2026-05-29",
                        "2026-05-30",
                        "2026-05-31",
                        "2026-06-01",
                        "2026-06-02",  #Fin hot sale

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

            if len(df_filtrado) < 2 or df_filtrado["y"].notna().sum() < 2:
                # Fallback para baja frecuencia histórica: promedio diario de ventas por días de predicción
                total_dias_hist = (self.df_historico["ds"].max() - self.df_historico["ds"].min()).days
                total_dias_hist = max(total_dias_hist, 1)
                total_ventas = df_filtrado["y"].sum()
                ventas_promedio_diaria = total_ventas / total_dias_hist
                dias_pred = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
                dias_pred = max(dias_pred, 1)
                total_estimado = ventas_promedio_diaria * dias_pred
            else:
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

            if len(df_articulo) < 2 or df_articulo["y"].notna().sum() < 2:
                # Fallback para baja frecuencia histórica
                total_dias_hist = (self.df_historico["ds"].max() - self.df_historico["ds"].min()).days
                total_dias_hist = max(total_dias_hist, 1)
                total_ventas = df_articulo["y"].sum()
                ventas_promedio_diaria = total_ventas / total_dias_hist
                dias_pred = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
                dias_pred = max(dias_pred, 1)
                total_estimado = ventas_promedio_diaria * dias_pred
            else:
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

                if len(df_entrenamiento) < 2 or df_entrenamiento["y"].notna().sum() < 2:
                    # Fallback para métricas en conjuntos de entrenamiento extremadamente pequeños
                    total_dias_entrenamiento = (df_entrenamiento["ds"].max() - df_entrenamiento["ds"].min()).days
                    total_dias_entrenamiento = max(total_dias_entrenamiento, 1)
                    total_ventas_entrenamiento = df_entrenamiento["y"].sum()
                    ventas_promedio_diaria_ent = total_ventas_entrenamiento / total_dias_entrenamiento
                    y_predicho = np.full(len(df_test), ventas_promedio_diaria_ent)
                else:
                    modelo_test = Prophet(holidays=self.feriados)
                    modelo_test.fit(df_entrenamiento[["ds", "y"]])
                    prediccion_test = modelo_test.predict(df_test[["ds"]])
                    y_predicho = prediccion_test["yhat"].values

                y_real = df_test["y"].values
                y_predicho = np.clip(y_predicho, 0, None)

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
