import flet as ft
import io
import base64
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os


def crear_vista_reportes(page: ft.Page, ultima_prediccion=None, ultima_metrica=None):
    # Colores principales de la interfaz base
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
                border=ft.border.all(1, card_border),
                shadow=ft.BoxShadow(
                    blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3)
                ),
                margin=ft.margin.only(bottom=20),
            )

        # Crear filas de la tabla de métricas
        filas_metricas = []
        if ultima_metrica is not None and len(ultima_metrica) > 0:
            for _, row in ultima_metrica.iterrows():
                filas_metricas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row["Producto"]), size=12)),
                            ft.DataCell(ft.Text(str(row["MAE"])), size=12),
                            ft.DataCell(ft.Text(str(row["RMSE"])), size=12),
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
            border=ft.border.all(1, card_border),
            shadow=ft.BoxShadow(
                blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3)
            ),
            margin=ft.margin.only(bottom=20),
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
                ft.Container(
                    content=ft.Row(
                        [
                            ft.ElevatedButton(
                                "SEMANAL",
                                color=primary,
                                bgcolor=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=6)
                                ),
                            ),
                            ft.TextButton(
                                "MENSUAL", style=ft.ButtonStyle(color=secondary)
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor="#f2f3ff",
                    border_radius=8,
                    padding=5,
                    border=ft.border.all(1, "#dae2fd"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
        margin=ft.margin.only(bottom=20),
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
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
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
            border=ft.border.all(1, card_border),
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

    # Gráfica Principal: Tendencias de Ventas (Guardando Matplotlib image localmente)
    def generar_grafico_lineas():
        import os

        fig, ax = plt.subplots(figsize=(10, 3.5), facecolor="white")
        meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO"]
        real = [50, 80, 40, 120, 90, 180, 140]  # Solo hasta julio
        proyectado = [70, 100, 60, 140, 110, 200, 160, 220]

        ax.plot(
            meses,
            proyectado,
            color="#cbd5e1",
            linestyle="--",
            linewidth=2,
            marker="o",
            label="Proyectado",
        )
        ax.plot(meses[:7], real, color="#0058be", linewidth=3, marker="o", label="Real")
        ax.plot(
            meses[5:],
            [180, 140, 190],
            color="#ef4444",
            linewidth=2.5,
            marker="o",
            label="Predicción",
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#cbd5e1")
        ax.spines["bottom"].set_color("#cbd5e1")
        ax.tick_params(colors="#505f76", labelsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_ylim(bottom=0)

        ax.legend(
            frameon=False, loc="upper right", ncol=3, fontsize=9, labelcolor="#505f76"
        )
        plt.tight_layout()

        filepath = os.path.abspath("tendencia.png")
        plt.savefig(filepath, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        return filepath

    # fin-generar_graficos_lineas

    tendencias_chart = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Tendencias de Ventas Mensuales",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=text_on_bg,
                ),
                ft.Text("Proyección vs Realidad 2024", size=14, color=secondary),
                ft.Container(height=10),
                ft.Image(src=generar_grafico_lineas(), fit="contain", expand=True),
            ]
        ),
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=12,
        border=ft.border.all(1, card_border),
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
        ),
        height=380,
        margin=ft.margin.only(top=20, bottom=20),
    )

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

    top_productos = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Top Productos",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=text_on_bg,
                        ),
                        ft.Text(
                            "RENDIMIENTO TOTAL ESTE MES",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=secondary,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=10),
                crear_barra_producto("Cerveza Pacífico", "$1.2M", 0.9),
                crear_barra_producto("Hielo en Bolsa", "$840K", 0.7),
                crear_barra_producto("Bloqueador Solar", "$620K", 0.55),
                crear_barra_producto("Coca-Cola 3L", "$410K", 0.35),
                crear_barra_producto("Botanas Surtidas", "$290K", 0.25),
            ],
            spacing=15,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=12,
        border=ft.border.all(1, card_border),
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
        ),
        margin=ft.margin.only(bottom=20),
    )

    # Tabla de Historial Reciente
    tabla_reportes = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Reportes Recientes",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=text_on_bg,
                        ),
                        ft.TextButton(
                            "Ver todos >", style=ft.ButtonStyle(color=primary)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(
                            ft.Text(
                                "NOMBRE DEL REPORTE",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=secondary,
                            )
                        ),
                        ft.DataColumn(
                            ft.Text(
                                "GENERADO POR",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=secondary,
                            )
                        ),
                        ft.DataColumn(
                            ft.Text(
                                "FECHA",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=secondary,
                            )
                        ),
                        ft.DataColumn(
                            ft.Text(
                                "ESTADO",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=secondary,
                            )
                        ),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.DESCRIPTION,
                                                color=primary,
                                                size=16,
                                            ),
                                            ft.Text("Ventas Q3 - Consolidado"),
                                        ]
                                    )
                                ),
                                ft.DataCell(
                                    ft.Text("Admin Sistema", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Text("Oct 12, 2024", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "Completado",
                                            size=12,
                                            color=ft.Colors.GREEN_700,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        bgcolor=ft.Colors.GREEN_100,
                                        padding=ft.padding.symmetric(
                                            horizontal=10, vertical=2
                                        ),
                                        border_radius=15,
                                    )
                                ),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.ANALYTICS,
                                                color=primary,
                                                size=16,
                                            ),
                                            ft.Text("Análisis de Demanda - Invierno"),
                                        ]
                                    )
                                ),
                                ft.DataCell(
                                    ft.Text("Admin Sistema", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Text("Oct 10, 2024", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "Completado",
                                            size=12,
                                            color=ft.Colors.GREEN_700,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        bgcolor=ft.Colors.GREEN_100,
                                        padding=ft.padding.symmetric(
                                            horizontal=10, vertical=2
                                        ),
                                        border_radius=15,
                                    )
                                ),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.SHOW_CHART,
                                                color=primary,
                                                size=16,
                                            ),
                                            ft.Text("Pronóstico de Ventas Q4"),
                                        ]
                                    )
                                ),
                                ft.DataCell(
                                    ft.Text("Admin Sistema", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Text("Oct 08, 2024", color=secondary, size=14)
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "En proceso",
                                            size=12,
                                            color=ft.Colors.ORANGE_700,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        bgcolor=ft.Colors.ORANGE_100,
                                        padding=ft.padding.symmetric(
                                            horizontal=10, vertical=2
                                        ),
                                        border_radius=15,
                                    )
                                ),
                            ]
                        ),
                    ],
                    expand=True,
                    heading_row_color=ft.Colors.GREY_50,
                ),
            ]
        ),
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=12,
        border=ft.border.all(1, card_border),
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)
        ),
    )  # fin-tabla_reportes

    # Contenedor padre general (scrollable)
    contenido_principal = ft.Column(
        [
            titulo,
            kpis,
            tendencias_chart,
            crear_seccion_metricas(),
            top_productos,
            tabla_reportes,
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
