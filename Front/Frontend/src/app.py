import flet as ft

def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    page.bgcolor = "white"

    titulo:str = 'Gestor de Inventario'
    txtDescripcion:str = 'Bienvenido a tu Gestor de Inventario Retail'
    
    page.add( ft.Text(titulo, color = ft.Colors.BLUE, size = 28) )
    page.add( ft.Divider(thickness = 5, color = "black") )
    page.add( ft.Text(txtDescripcion, color = ft.Colors.BLACK) )
    page.add( ft.Divider(height = 40, opacity = 1) )
    
    campos = ft.Column(
        controls = [
            ft.ElevatedButton("Procesadores", color = "white", width = 150),
            ft.ElevatedButton("Memorias RAM", color = "white", width = 150),
            ft.ElevatedButton("Fuentes de Poder", color = "white", width = 150),
            ft.ElevatedButton("Tarjetas Grafica", color = "white", width = 150),
        ],
        spacing = 30,
    )
    page.add(campos)
    
    tablaInventario = ft.DataTable(
        columns = [
            ft.DataColumn( ft.Text("Producto") ),
            ft.DataColumn( ft.Text("Categoria") ),
            ft.DataColumn( ft.Text("Precio") ),
            ft.DataColumn( ft.Text("Stock") )
        ],
        rows = [
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("AMD Ryzen 5 5600X") ),
                    ft.DataCell( ft.Text("Procesador") ),
                    ft.DataCell( ft.Text("3200") ),
                    ft.DataCell( ft.Text("20") )
                ]
            )
        ],
    )
    
    page.add(tablaInventario)


ft.run( main )