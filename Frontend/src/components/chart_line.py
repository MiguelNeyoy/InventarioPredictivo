import flet as ft
from flet_charts import LineChart, LineChartDataPoint, LineChartDataSet


def crear_grafico_linea(df_historico=None, df_prediccion=None, titulo="Tendencia de Ventas"):
    datasets = []

    if df_historico is not None and not df_historico.empty:
        df_historico = df_historico.sort_values("ds")
        puntos_historico = []
        for i, (_, row) in enumerate(df_historico.iterrows()):
            puntos_historico.append(LineChartDataPoint(x=i, y=float(row.get("y", 0))))

        if puntos_historico:
            datasets.append(
                LineChartDataSet(
                    data_points=puntos_historico,
                    color="#0058be",
                    label="Histórico",
                    stroke_width=2,
                    point_size=0,
                )
            )

    if df_prediccion is not None and not df_prediccion.empty:
        df_prediccion = df_prediccion.sort_values("Venta_Estimada")
        puntos_prediccion = []
        max_x = len(df_historico) if df_historico is not None else 0

        for i, (_, row) in enumerate(df_prediccion.iterrows()):
            puntos_prediccion.append(
                LineChartDataPoint(x=max_x + i, y=float(row.get("Venta_Estimada", 0)))
            )

        if puntos_prediccion:
            datasets.append(
                LineChartDataSet(
                    data_points=puntos_prediccion,
                    color="#ef4444",
                    label="Predicción",
                    stroke_width=2,
                    point_size=0,
                )
            )

    if not datasets:
        puntos_default = [
            LineChartDataPoint(x=0, y=50),
            LineChartDataPoint(x=1, y=80),
            LineChartDataPoint(x=2, y=40),
            LineChartDataPoint(x=3, y=120),
            LineChartDataPoint(x=4, y=90),
            LineChartDataPoint(x=5, y=180),
            LineChartDataPoint(x=6, y=140),
        ]
        datasets.append(
            LineChartDataSet(
                data_points=puntos_default,
                color="#0058be",
                label="Sin datos",
                stroke_width=2,
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                ft.LineChart(
                    data_series=datasets,
                    width=500,
                    height=250,
                    min_y=0,
                    interactive=True,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        expand=True,
    )


def crear_grafico_tendencia_simple():
    puntos = [
        LineChartDataPoint(x=0, y=50),
        LineChartDataPoint(x=1, y=80),
        LineChartDataPoint(x=2, y=40),
        LineChartDataPoint(x=3, y=120),
        LineChartDataPoint(x=4, y=90),
        LineChartDataPoint(x=5, y=180),
        LineChartDataPoint(x=6, y=140),
    ]

    return LineChart(
        data_series=[
            LineChartDataSet(
                data_points=puntos,
                color="#0058be",
                label="Ventas",
                stroke_width=2,
            )
        ],
        width=400,
        height=200,
        min_y=0,
    )