import flet as ft
import flet_charts as fch


def crear_grafico_barras(df_predicciones=None, titulo="Ventas por Producto", max_articulos=None):
    grupos = []
    etiquetas = []

    if df_predicciones is not None and not df_predicciones.empty:
        df_data = df_predicciones
        if max_articulos is not None:
            df_data = df_predicciones.head(max_articulos)
        
        for idx, (_, row) in enumerate(df_data.iterrows()):
            producto = str(row.get("Producto", ""))
            # Truncamos a 10 letras para legibilidad en la etiqueta
            nombre_corto = producto[:10] + ".." if len(producto) > 10 else producto
            etiquetas.append((idx, nombre_corto))
            valor = float(row.get("Venta_Estimada", 0))
            grupos.append(
                fch.BarChartGroup(
                    x=idx,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=valor,
                            width=30,
                            color="#0058be",
                            tooltip=fch.BarChartRodTooltip(
                                text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)
                            ),
                        ),
                    ],
                )
            )
    else:
        etiquetas_def = ["Ene", "Feb", "Mar", "Abr", "May"]
        for idx, etiqueta in enumerate(etiquetas_def):
            etiquetas.append((idx, etiqueta))
        grupos = [
            fch.BarChartGroup(x=0, rods=[fch.BarChartRod(from_y=0, to_y=50, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)))]),
            fch.BarChartGroup(x=1, rods=[fch.BarChartRod(from_y=0, to_y=80, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)))]),
            fch.BarChartGroup(x=2, rods=[fch.BarChartRod(from_y=0, to_y=40, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)))]),
            fch.BarChartGroup(x=3, rods=[fch.BarChartRod(from_y=0, to_y=120, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)))]),
            fch.BarChartGroup(x=4, rods=[fch.BarChartRod(from_y=0, to_y=90, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD)))]),
        ]

    # Crear etiquetas para el bottom axis
    eje_x_labels = []
    for idx, etiqueta in etiquetas:
        eje_x_labels.append(
            fch.ChartAxisLabel(
                value=idx,
                label=ft.Text(etiqueta, size=10, weight=ft.FontWeight.W_500, color="#505f76")
            )
        )

    # Calcular ancho dinámico: mínimo 600px, 75px por producto
    ancho_grafico = max(600, len(grupos) * 75)

    chart = fch.BarChart(
        groups=grupos,
        bottom_axis=fch.ChartAxis(
            labels=eje_x_labels,
            show_labels=True,
            label_size=30,
        ),
        interactive=True,
        width=ancho_grafico,
        expand=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=ft.Row(
                        controls=[chart],
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                    ),
                    height=200,
                    expand=True,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        expand=True,
    )


def crear_grafico_contraste(df_contraste=None, titulo="Real vs Estimado"):
    """
    Gráfico de barras agrupadas: una barra azul (Venta_Real) y una roja (Venta_Estimada)
    por producto. df_contraste debe tener: Producto, Venta_Real, Venta_Estimada.
    """
    grupos = []
    etiquetas = []

    if df_contraste is not None and not df_contraste.empty:
        for idx, (_, row) in enumerate(df_contraste.iterrows()):
            producto = str(row.get("Producto", ""))
            nombre_corto = producto[:10] + ".." if len(producto) > 10 else producto
            etiquetas.append((idx, nombre_corto))
            real = float(row.get("Venta_Real", 0))
            estimado = float(row.get("Venta_Estimada", 0))
            grupos.append(
                fch.BarChartGroup(
                    x=idx,
                    rods=[
                        fch.BarChartRod(from_y=0, to_y=real, width=30, color="#0058be", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD))),
                        fch.BarChartRod(from_y=0, to_y=estimado, width=30, color="#ef4444", tooltip=fch.BarChartRodTooltip(text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD))),
                    ],
                )
            )

    eje_x_labels = []
    for idx, etiqueta in etiquetas:
        eje_x_labels.append(
            fch.ChartAxisLabel(
                value=idx,
                label=ft.Text(etiqueta, size=10, weight=ft.FontWeight.W_500, color="#505f76")
            )
        )

    ancho_grafico = max(600, len(grupos) * 85)
    chart = fch.BarChart(
        groups=grupos,
        bottom_axis=fch.ChartAxis(labels=eje_x_labels, show_labels=True, label_size=30),
        interactive=True,
        width=ancho_grafico,
        expand=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                        ft.Row(
                            controls=[
                                ft.Row([ft.Container(width=12, height=12, bgcolor="#0058be", border_radius=2), ft.Text("Real", size=11)]),
                                ft.Row([ft.Container(width=12, height=12, bgcolor="#ef4444", border_radius=2), ft.Text("Estimado", size=11)]),
                            ],
                            spacing=15,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Row(controls=[chart], scroll=ft.ScrollMode.ALWAYS, expand=True),
                    height=200,
                    expand=True,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        expand=True,
    )


def crear_top_productos_chart(df_predicciones=None):
    if df_predicciones is None or df_predicciones.empty:
        return ft.Container(
            content=ft.Text("No hay datos de productos", color=ft.Colors.GREY),
            padding=20,
        )

    df_top = df_predicciones.sort_values("Venta_Estimada", ascending=False).head(5)

    def crear_barra_producto(nombre, monto, porcentaje):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(nombre, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text(monto, size=12, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(
                    value=porcentaje,
                    color="#0058be",
                    bgcolor="#eaedff",
                    height=10,
                    border_radius=5,
                ),
            ],
            spacing=5,
        )

    max_venta = df_top["Venta_Estimada"].max() if df_top["Venta_Estimada"].max() > 0 else 1
    barras = []

    for _, row in df_top.iterrows():
        porcentaje = float(row["Venta_Estimada"]) / float(max_venta) if max_venta > 0 else 0
        barras.append(
            crear_barra_producto(
                str(row["Producto"]),
                f"${row['Venta_Estimada']:,.0f}",
                porcentaje
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Top Productos", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("MAYOR DEMANDA", size=10, weight=ft.FontWeight.BOLD, color="#505f76"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=10),
                ft.Column(controls=barras, spacing=15),
            ],
            spacing=5,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        expand=True,
    )