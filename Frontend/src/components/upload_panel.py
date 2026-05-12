import flet as ft


def crear_upload_panel(
    campo_dias,
    slider_umbral,
    texto_umbral_label,
    texto_estado_ventas,
    texto_estado_stock,
    texto_estado,
    texto_parametros,
    abrir_dialogo_ventas,
    abrir_dialogo_stock,
    procesar_prediccion,
    exportar_csv=None,
):
    boton_exportar = ft.Button(
        content=ft.Row([ft.Icon(ft.Icons.DOWNLOAD), ft.Text("Exportar CSV")]),
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click = exportar_csv,
        width=150,
        height=40,
        disabled = True,
    )

    panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Controles de Filtro",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_500,
                ),
                ft.Container(height=10),
                ft.Row([campo_dias, ft.Text("días")], spacing=10),
                ft.Container(height=10),
                ft.Row([slider_umbral, texto_umbral_label], spacing=10),
                ft.Container(height=15),
                ft.Button(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.UPLOAD_FILE), ft.Text("Cargar Archivo de Ventas")]
                    ),
                    on_click=abrir_dialogo_ventas,
                ),
                texto_estado_ventas,
                ft.Container(height=10),
                ft.Button(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.INVENTORY_2), ft.Text("Cargar Archivo de Stock (OBLIGATORIO)")]
                    ),
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_600,
                    on_click=abrir_dialogo_stock,
                ),
                texto_estado_stock,
                ft.Container(height=15),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Row([ft.Icon(ft.Icons.PLAY_ARROW), ft.Text("Procesar Predicción")]),
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            on_click=procesar_prediccion,
                            width=180,
                            height=40,
                        ),
                        boton_exportar,
                    ],
                    spacing=10,
                ),
            ]
        ),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
    )

    return panel, boton_exportar