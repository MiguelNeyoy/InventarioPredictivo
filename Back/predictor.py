import pandas as pd
from prophet import Prophet


class MotorInventario:
    """
    Motor predictivo de inventario utilizando Prophet.
    Recibe un DataFrame unificado y genera pronósticos para períodos específicos.
    """

    def __init__(self, df_unificado):
        print("Iniciando Motor de IA para Inventario...")
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
        print(f"Generando pronóstico desde {start_date} hasta {end_date}...")
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
