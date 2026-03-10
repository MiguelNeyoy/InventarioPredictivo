import flet as ft
import csv #  <-- Esta libreria permite leer los arvhicos csv.

def main(page: ft.Page):
    
    '''
    carpeta = ft.FilePicker()
    page.overlay.append(carpeta)
    
    #Funcion para abrir el Explorardor de Archivos de Windows
    async def abrirExploradorDeArchivos(e):
        await carpeta.pick_files(
            allow_multiple=False,
            allowed_extensions= ["csv"]
        )
    '''
    
    # 1. Configuración principal de la página
    page.title = "Gestor de Inventario Predictivo"
    page.bgcolor = "#F4F6F8" 
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT 

    # 2. Encabezado (Título y Descripción)
    header = ft.Row(
        controls=[
            # ¡Ahora sí con Mayúsculas en Icons y Colors!
            ft.Icon(ft.Icons.INVENTORY, color=ft.Colors.BLUE_700, size=40),
            ft.Text("Gestor de Inventario Retail", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
        ],
        alignment=ft.MainAxisAlignment.START
    )
    subtitle = ft.Text("Bienvenido a tu panel de control. Selecciona una categoría o genera una predicción.", color=ft.Colors.BLUE_GREY_500)
    
    # 3. Menú Lateral (Sidebar)
    menu_botones = ft.Column(
        controls=[
            ft.Text("Categorías", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
            ft.Button("Procesadores", icon=ft.Icons.MEMORY, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
            ft.Button("Memorias RAM", icon=ft.Icons.MEMORY, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
            ft.Button("Fuentes de Poder", icon=ft.Icons.POWER, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
            ft.Button("Tarjetas Gráficas", icon=ft.Icons.MONITOR, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
            
            ft.Divider(height=30), 
            
            ft.Text("Inteligencia Artificial", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
            ft.Button("Predecir Demanda", icon=ft.Icons.AUTO_GRAPH, width=200, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        ],
        spacing=15,
    )

    sidebar = ft.Container(
        content=menu_botones,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
    )
    
    # 4. Tabla de Inventario
    '''
    filas = []
    
    with open('datosCSV.csv', 'r', encoding="utf-8") as inventario:
        columna = csv.reader(inventario)
    
        for fila in columna:
            filas.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text( fila[0] )),
                        ft.DataCell(ft.Text( fila[1] )),
                        ft.DataCell(ft.Text( fila[2] )),
                        ft.DataCell(ft.Text( fila[3] ))
                    ]
                )
            )    
    '''
    tabla_inventario = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio ($)", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock Actual", weight=ft.FontWeight.BOLD), numeric=True)
        ],
        rows= [],
        
        border=ft.Border.all(1, ft.Colors.GREY_200),
        border_radius=5,
        heading_row_color=ft.Colors.GREY_50,
        expand=True 
    )

    tabla_container = ft.Container(
        content=tabla_inventario,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
        expand=True 
    )

    # 5. Ensamblaje Final
    cuerpo_dashboard = ft.Row(
        controls=[
            sidebar,
            tabla_container
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )
    
    page.add(
        header, 
        subtitle, 
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), 
        cuerpo_dashboard
    )

ft.run( main )