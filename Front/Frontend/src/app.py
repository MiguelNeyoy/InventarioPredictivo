import flet as ft

def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    page.bgcolor = "white"

    titulo:str = 'Gestor de Inventario'
    page.add( ft.Text(titulo, color = ft.Colors.BLUE, size = 28) )
    
    page.add( ft.SearchBar(bar_hint_text="Buscar") )
    
    txtDescripcion:str = 'Bienvenido a tu Gestor de Inventario Retail'
    page.add( ft.Text(txtDescripcion, color = ft.Colors.BLACK) )
    
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