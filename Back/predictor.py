import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet optimizado.
    Recibe un DataFrame unificado y genera pronósticos para períodos específicos.
    """

    def __init__(self, df_unificado):
        self.df_historico = df_unificado
        
        # Generar feriados expandidos para 2023-2026 de Mazatlán e Internet (Hot Sale)
        feriados_lista = []
        for anio in [2023, 2024, 2025, 2026]:
            # Carnaval Mazatlán
            carnaval_dates = {
                2023: ["2023-02-19", "2023-02-20", "2023-02-21"],
                2024: ["2024-02-11", "2024-02-12", "2024-02-13"],
                2025: ["2025-03-02", "2025-03-03", "2025-03-04"],
                2026: ["2026-02-15", "2026-02-16", "2026-02-17"],
            }[anio]
            # Semana Santa
            semana_santa_dates = {
                2023: ["2023-04-02", "2023-04-03", "2023-04-04", "2023-04-05", "2023-04-06", "2023-04-07", "2023-04-08"],
                2024: ["2024-03-24", "2024-03-25", "2024-03-26", "2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30"],
                2025: ["2025-04-13", "2025-04-14", "2025-04-15", "2025-04-16", "2025-04-17", "2025-04-18", "2025-04-19"],
                2026: ["2026-03-30", "2026-03-31", "2026-04-01", "2026-04-02", "2026-04-03", "2026-04-04"],
            }[anio]
            # Infomatrix Pacífico
            infomatrix_dates = {
                2023: ["2023-02-09", "2023-02-10", "2023-02-11"],
                2024: ["2024-02-08", "2024-02-09", "2024-02-10"],
                2025: ["2025-02-06", "2025-02-07", "2025-02-08"],
                2026: ["2026-02-05", "2026-02-06", "2026-02-07"],
            }[anio]
            # Hot Sale
            hotsale_dates = {
                2023: [f"2023-05-{d}" for d in range(29, 32)] + [f"2023-06-0{d}" for d in range(1, 7)],
                2024: [f"2024-05-{d}" for d in range(15, 24)],
                2025: [f"2025-05-{d}" for d in range(15, 24)],
                2026: [f"2026-05-{d}" for d in range(25, 32)] + ["2026-06-01", "2026-06-02"],
            }[anio]
            
            for d in carnaval_dates:
                feriados_lista.append({"holiday": "carnaval_mazatlan", "ds": d, "lower_window": -1, "upper_window": 1})
            for d in semana_santa_dates:
                feriados_lista.append({"holiday": "semana_santa_mazatlan", "ds": d, "lower_window": -1, "upper_window": 1})
            for d in infomatrix_dates:
                feriados_lista.append({"holiday": "infomatrix_pacific", "ds": d, "lower_window": -1, "upper_window": 1})
            for d in hotsale_dates:
                feriados_lista.append({"holiday": "hot_sale", "ds": d, "lower_window": -1, "upper_window": 1})
        
        self.feriados = pd.DataFrame(feriados_lista)
        self.feriados["ds"] = pd.to_datetime(self.feriados["ds"])

    def _preparar_serie_temporal(self, df_producto, articulo):
        """
        Ordena cronológicamente la serie y asegura continuidad diaria rellenando días sin ventas con 0.
        """
        if df_producto.empty:
            return df_producto
            
        df_sorted = df_producto.sort_values("ds").copy()
        min_date = df_sorted["ds"].min()
        max_date = df_sorted["ds"].max()
        
        if min_date == max_date:
            # Si solo hay un punto de fecha, agregamos un punto inicial artificial con 0 ventas para permitir Prophet
            min_date = min_date - pd.Timedelta(days=30)
            df_sorted = pd.concat([
                pd.DataFrame({"ds": [min_date], "Producto": [articulo], "y": [0.0]}),
                df_sorted
            ], ignore_index=True)
            
        # Agrupar duplicados en el mismo día por si acaso
        df_grouped = df_sorted.groupby("ds")["y"].sum().reset_index()
        
        # Generar rango diario continuo
        rango_diario = pd.date_range(start=min_date, end=max_date, freq="D")
        df_continuo = df_grouped.set_index("ds").reindex(rango_diario, fill_value=0.0).reset_index()
        df_continuo = df_continuo.rename(columns={"index": "ds"})
        df_continuo["Producto"] = articulo
        return df_continuo

    def generar_prediccion(self, start_date, end_date):
        """
        Genera pronóstico para un periodo específico usando los datos históricos continuos optimizados.
        """
        resultados = []
        lista_productos = self.df_historico["Producto"].unique()

        for articulo in lista_productos:
            df_filtrado = self.df_historico[
                self.df_historico["Producto"] == articulo
            ].copy()

            # Asegurar serie temporal diaria continua con relleno de ceros
            df_filtrado = self._preparar_serie_temporal(df_filtrado, articulo)

            # Si después de preparar no tiene suficientes puntos (ej. vacío), usamos promedio diario
            if len(df_filtrado) < 2 or df_filtrado["y"].notna().sum() < 2:
                total_dias_hist = (self.df_historico["ds"].max() - self.df_historico["ds"].min()).days
                total_dias_hist = max(total_dias_hist, 1)
                total_ventas = df_filtrado["y"].sum()
                ventas_promedio_diaria = total_ventas / total_dias_hist
                dias_pred = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
                dias_pred = max(dias_pred, 1)
                total_estimado = ventas_promedio_diaria * dias_pred
            else:
                # Configurar Prophet óptimo para datos esporádicos continuos
                modelo = Prophet(
                    holidays=self.feriados,
                    daily_seasonality=False,
                    weekly_seasonality=True,
                    yearly_seasonality=True,
                    changepoint_prior_scale=0.1
                )
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
                        max(0.0, total_estimado)
                    ),  # Evita valores negativos
                }
            )

        return pd.DataFrame(resultados)

    def generar_prediccion_y_metricas(self, start_date, end_date, dias_test=30):
        """
        Genera predicción y calcula MAE/RMSE usando una ventana de validación (test) temporal.
        """
        resultados = []
        metricas = []
        lista_productos = self.df_historico["Producto"].unique()

        for articulo in lista_productos:
            df_articulo = self.df_historico[
                self.df_historico["Producto"] == articulo
            ].copy()
            
            # Asegurar serie temporal diaria continua con relleno de ceros
            df_articulo = self._preparar_serie_temporal(df_articulo, articulo)

            if len(df_articulo) < 2 or df_articulo["y"].notna().sum() < 2:
                # Fallback simple
                total_dias_hist = (self.df_historico["ds"].max() - self.df_historico["ds"].min()).days
                total_dias_hist = max(total_dias_hist, 1)
                total_ventas = df_articulo["y"].sum()
                ventas_promedio_diaria = total_ventas / total_dias_hist
                dias_pred = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
                dias_pred = max(dias_pred, 1)
                total_estimado = ventas_promedio_diaria * dias_pred
            else:
                # Modelo de producción principal
                modelo = Prophet(
                    holidays=self.feriados,
                    daily_seasonality=False,
                    weekly_seasonality=True,
                    yearly_seasonality=True,
                    changepoint_prior_scale=0.1
                )
                modelo.fit(df_articulo[["ds", "y"]])

                futuro = pd.DataFrame(
                    {"ds": pd.date_range(start=start_date, end=end_date, freq="D")}
                )
                prediccion = modelo.predict(futuro)
                total_estimado = prediccion["yhat"].sum()

            resultados.append(
                {
                    "Producto": articulo,
                    "Venta_Estimada": round(max(0.0, total_estimado)),
                }
            )

            # Cálculo de métricas
            if len(df_articulo) > (dias_test + 10):
                df_entrenamiento = df_articulo.iloc[:-dias_test]
                df_test = df_articulo.iloc[-dias_test:]

                if len(df_entrenamiento) < 2 or df_entrenamiento["y"].notna().sum() < 2:
                    total_dias_entrenamiento = (df_entrenamiento["ds"].max() - df_entrenamiento["ds"].min()).days
                    total_dias_entrenamiento = max(total_dias_entrenamiento, 1)
                    total_ventas_entrenamiento = df_entrenamiento["y"].sum()
                    ventas_promedio_diaria_ent = total_ventas_entrenamiento / total_dias_entrenamiento
                    y_predicho = np.full(len(df_test), ventas_promedio_diaria_ent)
                else:
                    modelo_test = Prophet(
                        holidays=self.feriados,
                        daily_seasonality=False,
                        weekly_seasonality=True,
                        yearly_seasonality=True,
                        changepoint_prior_scale=0.1
                    )
                    modelo_test.fit(df_entrenamiento[["ds", "y"]])
                    prediccion_test = modelo_test.predict(df_test[["ds"]])
                    y_predicho = prediccion_test["yhat"].values

                y_real = df_test["y"].values
                y_predicho = np.clip(y_predicho, 0.0, None)

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
