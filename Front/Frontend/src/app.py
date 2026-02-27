import flet as ft


def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    
    page.add( ft.Text("Inventario", color = ft.Colors.BLUE, size = 28) )
    
    page.add(
        
        ft.Row(
            controls = [
                ft.Button("Procesadores", color = ft.Colors.WHITE ),
                ft.Button("Memorias RAM", color = ft.Colors.WHITE )
            ]
        ),#fin-Row
        ft.Row(
            controls = [
                ft.Button("Fuentes de Poder", color = ft.Colors.WHITE),
                ft.Button("Tarjetas Grafica", color = ft.Colors.WHITE)
            ]
        )#fin-Row
        
    )#fin-page.add
   

ft.run( main )