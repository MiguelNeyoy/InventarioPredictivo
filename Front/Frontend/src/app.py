import flet as ft

def main( page: ft.Page ):
    
    #Titulo Interfaz
    page.title = "Interfaz Grafica"
    page.bgcolor = "#65F7DB"

    titulo:str = 'Gestor de Inventario'
    txtDescripcion:str = 'Bienvenido a tu Gestor de Inventario Retail'
    
    page.add( ft.Text(titulo, color = ft.Colors.BLUE, size = 28) )
    page.add( ft.Divider(thickness = 5, color = "black") )
    page.add( ft.Text(txtDescripcion, color = ft.Colors.BLACK) )
    page.add( ft.Divider(height = 40, opacity = 1) )
    
    campos = ft.Column(
        controls = [
            ft.ElevatedButton("Procesadores", bgcolor = "#D4F4F9", color = "#6588F7", width = 150),
            ft.ElevatedButton("Memorias RAM", bgcolor = "#D4F4F9", color ="#6588F7", width = 150),
            ft.ElevatedButton("Fuentes de Poder", bgcolor = "#D4F4F9", color = "#6588F7", width = 150),
            ft.ElevatedButton("Tarjetas Grafica", bgcolor = "#D4F4F9", color = "#6588F7", width = 150),
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
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("AMD Ryzen 7 5800X3D") ),
                    ft.DataCell( ft.Text("Procesador") ),
                    ft.DataCell( ft.Text("5464") ),
                    ft.DataCell( ft.Text("17") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Corsair Vengeance 16GB DDR4") ),
                    ft.DataCell( ft.Text("Memoria RAM") ),
                    ft.DataCell( ft.Text("847") ),
                    ft.DataCell( ft.Text("29") )
                ]
            ),ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Corsair RM750x 750W Gold") ),
                    ft.DataCell( ft.Text("Fuente de Poder") ),
                    ft.DataCell( ft.Text("1674") ),
                    ft.DataCell( ft.Text("11") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Cooler Master MWE 650W Bronze") ),
                    ft.DataCell( ft.Text("Fuente de Poder") ),
                    ft.DataCell( ft.Text("924") ),
                    ft.DataCell( ft.Text("14") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("NVIDIA RTX 4060") ),
                    ft.DataCell( ft.Text("Tarjeta Grafica") ),
                    ft.DataCell( ft.Text("7487") ),
                    ft.DataCell( ft.Text("10") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("AMD RX 6700 XT") ),
                    ft.DataCell( ft.Text("Tarjeta Grafica") ),
                    ft.DataCell( ft.Text("5200") ),
                    ft.DataCell( ft.Text("5") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Intel Core i5 12400F") ),
                    ft.DataCell( ft.Text("Procesador") ),
                    ft.DataCell( ft.Text("4878") ),
                    ft.DataCell( ft.Text("17") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Intel Core i7 12700K") ),
                    ft.DataCell( ft.Text("Procesador") ),
                    ft.DataCell( ft.Text("6988") ),
                    ft.DataCell( ft.Text("16") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("G.Skill Trident Z 32GB DDR4") ),
                    ft.DataCell( ft.Text("Memoria RAM") ),
                    ft.DataCell( ft.Text("1612") ),
                    ft.DataCell( ft.Text("31") )
                ]
            ),
            ft.DataRow(
                cells = [
                    ft.DataCell( ft.Text("Crucial Ballistix 16GB DDR4") ),
                    ft.DataCell( ft.Text("Memoria RAM") ),
                    ft.DataCell( ft.Text("1244") ),
                    ft.DataCell( ft.Text("18") )
                ]
            ),
        ],
        border = ft.Border.all(2,"black"), 
        border_radius = 5,
        bgcolor = "white"
    )
    
    page.add(tablaInventario)


ft.run( main )