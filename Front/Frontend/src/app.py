import flet as ft


def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    
    page.add( ft.Text("Inventario") )
    
    page.add(
        
        ft.Row(
            controls = [
                ft.Button("Procesadores"),
                ft.Button("Memorias RAM")
            ]
        ),
        ft.Row(
            controls = [
                ft.Button("Fuentes de Poder"),
                ft.Button("Tarjetas Grafica")
            ]
        )
        
    )#fin-page.add
   

ft.run( main )