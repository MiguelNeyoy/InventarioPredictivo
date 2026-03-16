import flet as ft
import csv

def main(page: ft.Page):
    
    page.title = "Estación de Análisis Centralizada"
    page.bgcolor = "#F4F6F8" 
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.window_width = 1280
    page.window_height = 800

    '''
    # Se deja comentado el apartado para subir el CSV según la petición
    carpeta = ft.FilePicker()
    page.overlay.append(carpeta)
    
    #Funcion para abrir el Explorardor de Archivos de Windows
    async def abrirExploradorDeArchivos(e):
        await carpeta.pick_files(
            allow_multiple=False,
            allowed_extensions= ["csv", "xlsx"]
        )

    boton_subir_csv = ft.ElevatedButton(
        "Cargue sus datos de ventas (Arrastre su archivo CSV)",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=abrirExploradorDeArchivos
    )
    '''
    # Placeholder del botón comentado para mantener el diseño visual (comentado a nivel de UI)
    boton_subir_csv = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.UPLOAD_FILE, size=40, color=ft.Colors.BLUE_GREY_400),
            ft.Text("Cargue sus datos de ventas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
            ft.Text("Arrastre su archivo CSV o Excel para iniciar el análisis predictivo. (Funcionalidad Comentada)", color=ft.Colors.BLUE_GREY_400, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30,
        border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.WHITE
    )

    # Menú Lateral (Sidebar)
    sidebar_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.BLUE_700, size=30),
                    ft.Text("Predictor", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
                ]),
                padding=ft.padding.only(bottom=20)
            ),
            ft.Text("MENÚ PRINCIPAL", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_400),
            ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD), title=ft.Text("Panel de Control"), selected=True, on_click=lambda e: None),
            ft.ListTile(leading=ft.Icon(ft.Icons.ANALYTICS), title=ft.Text("Reportes"), on_click=lambda e: None),
            ft.ListTile(leading=ft.Icon(ft.Icons.COMPARE_ARROWS), title=ft.Text("Comparaciones"), on_click=lambda e: None),
            ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS), title=ft.Text("Configuración"), on_click=lambda e: None),
            ft.Divider(height=20),
            ft.Container(expand=True), # Spacer
        ],
        spacing=5,
        expand=True
    )

    sidebar = ft.Container(
        content=sidebar_content,
        width=250,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.only(top_right=15, bottom_right=15),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
    )

    # Contenido Principal
    header = ft.Container(
        content=ft.Text("Estación de Análisis Centralizada", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
        padding=ft.padding.only(bottom=20, top=20)
    )

    tarjetas_superiores = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("Tendencia Histórica", weight=ft.FontWeight.BOLD),
                ft.Icon(ft.Icons.SHOW_CHART, size=50, color=ft.Colors.BLUE_500)
            ]),
            bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, expand=True, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Proyección de Ingresos", weight=ft.FontWeight.BOLD),
                ft.Icon(ft.Icons.BAR_CHART, size=50, color=ft.Colors.GREEN_500)
            ]),
            bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, expand=True, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
        )
    ], spacing=20)

    vista_datos = ft.Container(
        content=ft.Column([
            ft.Text("Vista Previa de Datos Recientes", weight=ft.FontWeight.BOLD, size=18),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Producto")),
                    ft.DataColumn(ft.Text("Categoría")),
                    ft.DataColumn(ft.Text("Ventas"))
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("SaaS Tier 1")), ft.DataCell(ft.Text("Software")), ft.DataCell(ft.Text("150"))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("2")), ft.DataCell(ft.Text("API Gateway")), ft.DataCell(ft.Text("Infra")), ft.DataCell(ft.Text("85"))])
                ],
                expand=True
            )
        ]),
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12), margin=ft.padding.only(top=20)
    )

    metricas_clave = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER_500), ft.Text("Métricas Clave & Resumen del Sistema", weight=ft.FontWeight.BOLD, size=18)]),
            ft.Text("Se han detectado patrones de crecimiento sostenido en la categoría SaaS. La proyección para el Q4 muestra un incremento del 15%."),
            ft.Divider(height=20),
            ft.Text("Recomendaciones:", weight=ft.FontWeight.BOLD),
            ft.Text("• Aumentar stock para SaaS Tier 1."),
            ft.Text("• Revisar precios de API Gateway.")
        ]),
        bgcolor=ft.Colors.BLUE_50, padding=20, border_radius=10, margin=ft.padding.only(top=20)
    )

    columna_principal = ft.Column(
        controls=[
            header,
            ft.Text("Controles de Filtro", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_500),
            boton_subir_csv,
            ft.Container(height=10),
            tarjetas_superiores,
            vista_datos,
            metricas_clave
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    cuerpo_dashboard = ft.Row(
        controls=[
            sidebar,
            ft.Container(content=columna_principal, padding=30, expand=True)
        ],
        expand=True,
        spacing=0
    )
    
    page.add(cuerpo_dashboard)

ft.run( main )
