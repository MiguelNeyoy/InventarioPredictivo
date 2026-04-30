import flet as ft
import flet_charts as fch


def crear_grafico_linea(df_historico=None, df_prediccion=None, titulo="Tendencia de Ventas"):
    data_series = []

    if df_historico is not None and not df_historico.empty:
        df_historico = df_historico.sort_values("ds")
        puntos = []
        for i, (_, row) in enumerate(df_historico.iterrows()):
            puntos.append(fch.LineChartDataPoint(x=i, y=float(row.get("y", 0))))
        
        if puntos:
            data_series.append(
                fch.LineChartData(
                    points=puntos,
                    color="#0058be",
                    stroke_width=2,
                )
            )

    if df_prediccion is not None and not df_prediccion.empty:
        max_x = len(df_historico) if df_historico is not None else 0
        puntos = []
        
        for i, (_, row) in enumerate(df_prediccion.iterrows()):
            puntos.append(fch.LineChartDataPoint(x=max_x + i, y=float(row.get("Venta_Estimada", 0))))
        
        if puntos:
            data_series.append(
                fch.LineChartData(
                    points=puntos,
                    color="#ef4444",
                    stroke_width=2,
                )
            )

    if not data_series:
        puntos_default = [
            fch.LineChartDataPoint(x=0, y=50),
            fch.LineChartDataPoint(x=1, y=80),
            fch.LineChartDataPoint(x=2, y=40),
            fch.LineChartDataPoint(x=3, y=120),
            fch.LineChartDataPoint(x=4, y=90),
            fch.LineChartDataPoint(x=5, y=180),
            fch.LineChartDataPoint(x=6, y=140),
        ]
        data_series.append(
            fch.LineChartData(
                points=puntos_default,
                color="#0058be",
                stroke_width=2,
            )
        )

    chart = fch.LineChart(
        data_series=data_series,
        min_y=0,
        interactive=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=chart,
                    height=250,
                    expand=True,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        expand=True,
    )