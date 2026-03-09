import flet as ft

def main(page: ft.Page):

    page.title = ""
    page.bgcolor = "#f5f7fb"

    # Columna Lateral Izquierda
    columnaLateral = ft.Container(
        width=220,
        bgcolor="white",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Predicciones", size=20, weight="bold"),

                ft.Divider(),

                ft.Container(expand=True),
            ]
        )
    )
    
    
    #Boton para subir archivo .csv
    botonCSV = ft.Container(
        bgcolor="white",
        padding=15,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls = [ 
                
                ft.Row(
                    controls = [
                        ft.Button("Subir Archivo .csv")
                    ]
                )
            ]
        )
    )
    
    
    tablaInventario = ft.DataTable(
        columns = [
            ft.DataColumn( ft.Text("Articulo") ),
            ft.DataColumn( ft.Text("Categoria") ),
            ft.DataColumn( ft.Text("Precio") ),
            ft.DataColumn( ft.Text("Stock") )
        ]
    )
    
    diseñoTablaInventario = ft.Container(
        bgcolor= "",
        padding= 20,
        border_radius= 100,
        content = ft.Column(
            controls = [
                ft.Text("Inventario"),
                tablaInventario
            ]
        )
    )
            
    page.add(columnaLateral)
    page.add(botonCSV)
    page.add(diseñoTablaInventario)

ft.app(target=main)