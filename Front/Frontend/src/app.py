import flet as ft

def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    page.bgcolor = "white"

    titulo:str = 'Gestor de Inventario'
    txtDescripcion:str = 'Bienvenido a tu Gestor de Inventario Retail'
    
    page.add( ft.Text(titulo, color = ft.Colors.BLUE, size = 28) )
    page.add( ft.Text(txtDescripcion, color = ft.Colors.BLACK) )
   
    campos = ft.Column(
        spacing = 30,
        controls = [
            
            ft.Button("Procesadores", color = ft.Colors.WHITE ),
            ft.Button("Memorias RAM", color = ft.Colors.WHITE ),
            ft.Button("Fuentes de Poder", color = ft.Colors.WHITE),
            ft.Button("Tarjetas Grafica", color = ft.Colors.WHITE)
        ]
        
    )
    page.add(campos)


ft.run( main )