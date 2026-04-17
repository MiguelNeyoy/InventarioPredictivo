import flet as ft


def crear_tabla_resultados(df_alertas=None):
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Venta Estimada", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock Actual", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cant. Comprar", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Alerta"), weight=ft.FontWeight.BOLD),
        ],
        rows=[],
    )

    if df_alertas is not None and not df_alertas.empty:
        nuevas_filas = []
        for _, row in df_alertas.iterrows():
            alerta = row.get("Alerta_Surtir", False)
            color = ft.Colors.RED_50 if alerta else ft.Colors.GREEN_50
            alerta_icono = (
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED)
                if alerta
                else ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN)
            )

            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row.get("Producto", "")))),
                        ft.DataCell(ft.Text(str(row.get("Venta_Estimada", 0)))),
                        ft.DataCell(ft.Text(str(row.get("Stock_Actual", 0)))),
                        ft.DataCell(ft.Text(str(row.get("Cantidad_A_Comprar", 0)))),
                        ft.DataCell(alerta_icono),
                    ],
                    color=color,
                )
            )
        tabla.rows = nuevas_filas

    return tabla