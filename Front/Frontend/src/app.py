import flet as ft

def main(page: ft.Page):

    page.title = "Inventario Predictivo"
    page.bgcolor = "#65F7DB"

    # Columna Lateral Izquierda
    columnaLateral = ft.Container(
        width=220,
        bgcolor="white",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Predicciones", size=20, weight="bold", color = ft.Colors.BLUE),

                ft.Divider(),

                ft.Container(expand = True),
            ]
        )
    )
    
    
    #Boton para subir archivo .csv
    botonCSV = ft.Container(
        bgcolor = "white",
        padding = 15,
        content = ft.Row(
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            controls = [ 
                
                ft.Row(
                    controls = [
                        ft.Button("Subir Archivo .csv", color = "white", bgcolor = "#6588F7")
                    ]
                )
            ]
        )
    )
    
    #Tabla que visualiza el archivo .csv
    tablaInventario = ft.DataTable(
        columns = [
            ft.DataColumn( ft.Text("Articulo",color = "black") ),
            ft.DataColumn( ft.Text("Categoria", color = "black") ),
            ft.DataColumn( ft.Text("Precio", color = "black") ),
            ft.DataColumn( ft.Text("Stock", color = "black") )
        ]
    )
    
    #Sirve para añadir el diseño que tendra la tabla
    diseñoTablaInventario = ft.Container(
        bgcolor= "white",
        padding= 20,
        border_radius= 50,
        content = ft.Column(
            controls = [
                ft.Text("Inventario", color = "black"),
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
                                        ft.Text("Gestor de Inventario Predictivo", color = ft.Colors.BLUE),
                                        ft.Text("Bienvenido a tu gestor de invenatrio reatil.\nPuedes revisar tu inventario u tener una prediccion del mismo.", color= "black")
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