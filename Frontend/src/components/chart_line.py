import flet as ft
import flet_charts as fch


def crear_grafico_linea(df_historico=None, df_prediccion=None, titulo="Tendencia de Ventas"):
    data_series = []

    if df_historico is not None and not df_historico.empty:
        df_historico = df_historico.sort_values("ds")
        puntos = []
        for i, (_, row) in enumerate(df_historico.iterrows()):
            puntos.append(fch.LineChartDataPoint(i, float(row.get("y", 0))))
        
        if puntos:
            data_series.append(
                fch.LineChartData(
                    data_points=puntos,
                    color="#0058be",
                    label="Histórico",
                    stroke_width=2,
                )
            )

    if df_prediccion is not None and not df_prediccion.empty:
        max_x = len(df_historico) if df_historico is not None else 0
        puntos = []
        
        for i, (_, row) in enumerate(df_prediccion.iterrows()):
            puntos.append(fch.LineChartDataPoint(max_x + i, float(row.get("Venta_Estimada", 0))))
        
        if puntos:
            data_series.append(
                fch.LineChartData(
                    data_points=puntos,
                    color="#ef4444",
                    label="Predicción",
                    stroke_width=2,
                )
            )

    if not data_series:
        puntos_default = [
            fch.LineChartDataPoint(0, 50),
            fch.LineChartDataPoint(1, 80),
            fch.LineChartDataPoint(2, 40),
            fch.LineChartDataPoint(3, 120),
            fch.LineChartDataPoint(4, 90),
            fch.LineChartDataPoint(5, 180),
            fch.LineChartDataPoint(6, 140),
        ]
        data_series.append(
            fch.LineChartData(
                data_points=puntos_default,
                color="#0058be",
                label="Sin datos",
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