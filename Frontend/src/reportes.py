import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from components.chart_line import crear_grafico_linea
from components.chart_bar import crear_grafico_barras, crear_top_productos_chart
from components.chart_pie import crear_grafico_pastel


def crear_vista_reportes(page: ft.Page, ultima_prediccion=None, ultima_metrica=None, df_historico=None):
    bg_color = "#faf8ff"
    text_on_bg = "#131b2e"
    primary = "#0058be"
    secondary = "#505f76"
    card_border = "#f1f5f9"

    # Sección colapsable de métricas de predicción
    def crear_seccion_metricas():
        if ultima_metrica is None or len(ultima_metrica) == 0:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.ANALYTICS, color=primary, size=20),
                                ft.Text(
                                    "Métricas de Precisión del Modelo",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=text_on_bg,
                                ),
                                ft.Icon(ft.Icons.EXPAND_MORE, color=secondary, size=20),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Ejecute una predicción para ver las métricas de precisión (MAE/RMSE)",
                                size=14,
                                color=secondary,
                                italic=True,
                            ),
                            padding=10,
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=8,
                        ),
                    ]
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=12,
                border=ft.Border.all(1, card_border),
                shadow=ft.BoxShadow(
                    blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3)
                ),
                margin=ft.Margin.only(bottom=20),
            )

        # Crear filas de la tabla de métricas
        filas_metricas = []
        if ultima_metrica is not None and len(ultima_metrica) > 0:
            for _, row in ultima_metrica.iterrows():
                filas_metricas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row["Producto"]), size=12)),
                            ft.DataCell(ft.Text(str(row["MAE"]), size=12)),
                            ft.DataCell(ft.Text(str(row["RMSE"]), size=12)),
                        ]
                    )
                )

        else:
            filas_metricas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay datos", color=secondary)),
                        ft.DataCell(ft.Text("0", color=secondary)),
                        ft.DataCell(ft.Text("0", color=secondary)),
                    ]
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ANALYTICS, color=primary, size=20),
                            ft.Text(
                                "Métricas de Precisión del Modelo",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=text_on_bg,
                            ),
                            ft.Icon(ft.Icons.EXPAND_LESS, color=secondary, size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(
                                            ft.Text(
                                                "Producto",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            )
                                        ),
                                        ft.DataColumn(
                                            ft.Text(
                                                "MAE",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            )
                                        ),
                                        ft.DataColumn(
                                            ft.Text(
                                                "RMSE",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            )
                                        ),
                                    ],
                                    rows=filas_metricas,
                                    heading_row_color=ft.Colors.GREY_50,
                                    divider_thickness=1,
                                    horizontal_lines=ft.BorderSide(
                                        1, ft.Colors.GREY_300
                                    ),
                                )
                            ],
                            spacing=10,
                        ),
                        padding=10,
                    ),
                ]
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3)
            ),
            margin=ft.Margin.only(bottom=20),
        )

    # Encabezado "Centro de Reportes Analíticos"
    titulo = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Centro de Reportes Analíticos",
                            size=28,
                            weight=ft.FontWeight.W_800,
                            color=text_on_bg,
                        ),
                        ft.Text(
                            "Visualización de rendimiento estratégico para el periodo actual.",
                            color=secondary,
                            size=14,
                            weight=ft.FontWeight.W_500,
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
        margin=ft.Margin.only(bottom=20),
    )  # Fin-encabezado

    # Tarjetas KPI
    def crear_kpi_card(titulo, valor, porcentaje, icono, es_positivo):
        color_porcentaje = ft.Colors.GREEN_600 if es_positivo else ft.Colors.RED_500
        bg_porcentaje = ft.Colors.GREEN_50 if es_positivo else ft.Colors.RED_50

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(icono, color=primary, size=20),
                                padding=10,
                                bgcolor="#eff6fc",
                                border_radius=8,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    porcentaje,
                                    color=color_porcentaje,
                                    weight=ft.FontWeight.BOLD,
                                    size=12,
                                ),
                                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                                bgcolor=bg_porcentaje,
                                border_radius=4,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(
                        titulo, size=12, weight=ft.FontWeight.W_600, color=secondary
                    ),
                    ft.Text(
                        valor, size=24, weight=ft.FontWeight.W_800, color=text_on_bg
                    ),
                ],
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
            ),
            expand=True,
        )  # fin-crear_kpi_card

    # Determinar valores de KPI según datos disponibles
    if ultima_prediccion is not None and len(ultima_prediccion) > 0:
        num_articulos = str(len(ultima_prediccion))
        texto_articulos = f"{num_articulos} análisis"

        if ultima_metrica is not None and len(ultima_metrica) > 0:
            # Calcular promedio de MAE
            mae_promedio = ultima_metrica["MAE"].mean()
            acertividad = max(0, min(100, 100 - (mae_promedio * 10)))
            texto_acertividad = f"{acertividad:.1f}%"
        else:
            texto_acertividad = "Sin datos"
    else:
        texto_articulos = "0"
        texto_acertividad = "Sin datos"

    kpis = ft.Row(
        [
            crear_kpi_card(
                "ARTÍCULOS ANALIZADOS",
                texto_articulos,
                "0%",
                ft.Icons.INVENTORY_2,
                True,
            ),
            crear_kpi_card(
                "ACERTIVIDAD DEL MODELO",
                texto_acertividad,
                "0%",
                ft.Icons.VERIFIED,
                True,
            ),
        ],
        spacing=20,
    )

    

    # Gráficos desactivados temporalmente para diagnosticar alto CPU
    # grafico_tendencia = crear_grafico_linea(df_historico, ultima_prediccion, "Tendencias de Ventas")

    tendencias_chart = ft.Container()
    # tendencias_chart = ft.Container(
    #     content=ft.Column(
    #         controls=[
    #             ft.Text(
    #                 "Tendencias de Ventas Mensuales",
    #                 size=18,
    #                 weight=ft.FontWeight.BOLD,
    #                 color=text_on_bg,
    #             ),
    #             ft.Text("Proyección vs Realidad", size=14, color=secondary),
    #             ft.Container(height=10),
    #             grafico_tendencia,
    #         ]
    #     ),
    #     bgcolor=ft.Colors.WHITE,
    #     padding=30,
    #     border_radius=12,
    #     border=ft.border.all(1, card_border),
    #     shadow=ft.BoxShadow(
    #         blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
    #     ),
    #     height=380,
    #     margin=ft.margin.only(top=20, bottom=20),
    # )

    # Gráficas Secundarias: Top Productos
    def crear_barra_producto(nombre, monto, porcentaje_ancho):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            nombre, size=12, weight=ft.FontWeight.BOLD, color=secondary
                        ),
                        ft.Text(
                            monto, size=12, weight=ft.FontWeight.BOLD, color=secondary
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(
                    value=porcentaje_ancho,
                    color=primary,
                    bgcolor="#eaedff",
                    height=10,
                    border_radius=5,
                ),
            ],
            spacing=5,
        )

    # fin-crear_barra_productos

    # Gráficos desactivados temporalmente para diagnosticar alto CPU
    top_productos = None

    # if ultima_prediccion is not None and not ultima_prediccion.empty:
    #     top_productos = ft.Container(
    #         content=crear_top_productos_chart(ultima_prediccion),
    #         bgcolor=ft.Colors.WHITE,
    #         padding=30,
    #         border_radius=12,
    #         border=ft.border.all(1, card_border),
    #         shadow=ft.BoxShadow(
    #             blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
    #         ),
    #         margin=ft.margin.only(bottom=20),
    #     )

    # Gráfica de pastel de popularidad de productos (Demanda Estimada)
    if ultima_prediccion is not None and not ultima_prediccion.empty:
        grafico_pastel_completo = crear_grafico_pastel(
            ultima_prediccion,
            titulo="Popularidad de Productos (Demanda Estimada)"
        )
        seccion_grafico_pastel = ft.Container(
            content=grafico_pastel_completo,
            bgcolor=ft.Colors.WHITE,
            padding=10,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
            ),
            margin=ft.Margin.only(bottom=20),
        )
    else:
        seccion_grafico_pastel = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PIE_CHART, color=primary, size=20),
                            ft.Text(
                                "Popularidad de Productos (Demanda Estimada)",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=text_on_bg,
                            ),
                        ]
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Ejecute una predicción para observar la popularidad de productos",
                            size=14,
                            color=secondary,
                            italic=True,
                        ),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=8,
                    ),
                ]
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
            ),
            margin=ft.Margin.only(bottom=20),
        )

    # Gráfica de barras de todos los artículos predichos
    if ultima_prediccion is not None and not ultima_prediccion.empty:
        grafico_barras_completo = crear_grafico_barras(
            ultima_prediccion,
            titulo="Ventas Proyectadas por Artículo"
        )
        seccion_grafico_barras = ft.Container(
            content=grafico_barras_completo,
            bgcolor=ft.Colors.WHITE,
            padding=10,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
            ),
            margin=ft.Margin.only(bottom=20),
        )
    else:
        seccion_grafico_barras = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BAR_CHART, color=primary, size=20),
                            ft.Text(
                                "Ventas Proyectadas por Artículo",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=text_on_bg,
                            ),
                        ]
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Ejecute una predicción para observar la gráfica de barras de artículos",
                            size=14,
                            color=secondary,
                            italic=True,
                        ),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=8,
                    ),
                ]
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            border=ft.Border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
            ),
            margin=ft.Margin.only(bottom=20),
        )

    contenido_principal = ft.Column(
        [
            titulo,
            kpis,
            tendencias_chart,
            crear_seccion_metricas(),
            seccion_grafico_barras,
            top_productos if top_productos else ft.Container(),
            seccion_grafico_pastel,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Container(content=contenido_principal, expand=True, padding=0)


def main(page: ft.Page):
    page.title = "Reporte Analítico"
    page.bgcolor = "#faf8ff"
    page.padding = 30
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(crear_vista_reportes(page))


if __name__ == "__main__":
    ft.app(target=main)
