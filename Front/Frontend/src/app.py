import flet as ft

def main(page: ft.Page):

    page.title = ""
    page.bgcolor = ""

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
    
    #Tabla que visualiza el archivo .csv
    tablaInventario = ft.DataTable(
        columns = [
            ft.DataColumn( ft.Text("Articulo") ),
            ft.DataColumn( ft.Text("Categoria") ),
            ft.DataColumn( ft.Text("Precio") ),
            ft.DataColumn( ft.Text("Stock") )
        ]
    )
    
    #Sire para añadir el diseño que tendra la tabla
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
    
    
    menu = ft.Column(
        expand = True,
        controls = [
            
            botonCSV,
            
            ft.Container(
                padding = 20,
                content = ft.Column(
                    controls = [
                        ft.Row(
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls = [
                                ft.Column(
                                    controls = [
                                        ft.Text("Gestor de Inventario Predictivo"),
                                        ft.Text("Bienvenido a tu gestor de invenatrio reatil.\nPuedes revisar tu inventario u tener una prediccion del mismo.")
                                    ]
                                )
                            ]
                        ),
                        ft.Container(height = 20),
                        
                        diseñoTablaInventario
                    ]
                )
            )
        ]
    )
    
    
    #Visualiza el como debe de verse la interfaz
    page.add(
        ft.Row(
            expand = True,
            controls = [
                columnaLateral,
                menu
            ]
        )
    )

ft.run(main)