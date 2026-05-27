import flet as ft
import flet_charts as fch

def crear_grafico_pastel(df_predicciones=None, titulo="Popularidad de Productos (Demanda Estimada)"):
    if df_predicciones is None or df_predicciones.empty:
        # Default placeholder data if no predictions
        data = [
            ("Producto A", 120, "#0058be"),
            ("Producto B", 90, "#3b82f6"),
            ("Producto C", 60, "#10b981"),
            ("Producto D", 45, "#f59e0b"),
            ("Producto E", 30, "#ec4899"),
        ]
    else:
        # Sort and take top 5
        df_sorted = df_predicciones.sort_values("Venta_Estimada", ascending=False)
        total_ventas = df_sorted["Venta_Estimada"].sum()
        if total_ventas == 0:
            total_ventas = 1  # Avoid division by zero
            
        colores_palette = ["#0058be", "#3b82f6", "#10b981", "#f59e0b", "#ec4899"]
        
        data = []
        df_top = df_sorted.head(5)
        
        for idx, (_, row) in enumerate(df_top.iterrows()):
            prod = str(row["Producto"])
            ventas = float(row["Venta_Estimada"])
            if ventas > 0:
                color = colores_palette[idx % len(colores_palette)]
                data.append((prod, ventas, color))

    # Calculate total inside data
    suma_total = sum(item[1] for item in data)
    if suma_total == 0:
        suma_total = 1

    # Create PieChart sections
    sections = []
    legend_items = []

    for name, value, color in data:
        porcentaje = (value / suma_total) * 100
        label_title = f"{porcentaje:.0f}%" if porcentaje >= 5 else "" # Only show inside if large enough
        
        # Pie slice
        sections.append(
            fch.PieChartSection(
                value=value,
                title=label_title,
                color=color,
                radius=40,
                title_style=ft.TextStyle(
                    size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE
                ),
            )
        )
        
        # Legend item row
        legend_items.append(
            ft.Row(
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        bgcolor=color,
                        border_radius=6,
                    ),
                    ft.Text(name, size=12, weight=ft.FontWeight.W_500, expand=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"{value:,.0f} u. ({porcentaje:.1f}%)", size=11, weight=ft.FontWeight.BOLD, color="#505f76"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8,
            )
        )

    chart = fch.PieChart(
        sections=sections,
        sections_space=2,
        center_space_radius=40,
        expand=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        # Chart container
                        ft.Container(
                            content=chart,
                            width=180,
                            height=180,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(width=15),
                        # Legend container
                        ft.Column(
                            controls=legend_items,
                            spacing=8,
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
            ]
        ),
        padding=25,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        expand=True,
    )
