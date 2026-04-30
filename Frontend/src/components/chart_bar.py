import flet as ft
import flet_charts as fch


def crear_grafico_barras(df_predicciones=None, titulo="Ventas por Producto"):
    grupos = []
    etiquetas = []

    if df_predicciones is not None and not df_predicciones.empty:
        df_top = df_predicciones.head(10)
        
        for idx, (_, row) in enumerate(df_top.iterrows()):
            producto = str(row.get("Producto", ""))[:8]
            etiquetas.append(producto)
            valor = float(row.get("Venta_Estimada", 0))
            grupos.append(
                fch.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=valor,
                            width=40,
                            color="#0058be",
                            border_radius=0,
                        ),
                    ],
                )
            )
    else:
        etiquetas = ["Ene", "Feb", "Mar", "Abr", "May"]
        grupos = [
            fch.BarChartGroup(
                x=0,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=50, width=40, color="#0058be")],
            ),
            fch.BarChartGroup(
                x=1,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=80, width=40, color="#0058be")],
            ),
            fch.BarChartGroup(
                x=2,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=40, width=40, color="#0058be")],
            ),
            fch.BarChartGroup(
                x=3,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=120, width=40, color="#0058be")],
            ),
            fch.BarChartGroup(
                x=4,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=90, width=40, color="#0058be")],
            ),
        ]

    chart = fch.BarChart(
        bar_groups=grupos,
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