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
    
    page.add(columnaLateral)

ft.app(target=main)