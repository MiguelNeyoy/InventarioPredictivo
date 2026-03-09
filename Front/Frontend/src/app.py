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
    
    
    #
    topbar = ft.Container(
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
            
    page.add(columnaLateral)
    page.add(topbar)

ft.app(target=main)