import sys
import os
import threading
import flet as ft
import pandas as pd

# Adicionando el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Back.predictor import MotorInventario
from reportes import crear_vista_reportes

def main(page: ft.Page):
    
    page.title = "Estación de Análisis Centralizada"
    page.bgcolor = "#F4F6F8" 
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.window_width = 1280
    page.window_height = 800

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Venta Estimada (15 días)")),
            ft.DataColumn(ft.Text("Stock Actual")),
            ft.DataColumn(ft.Text("Cant. Comprar")),
            ft.DataColumn(ft.Text("Alerta"))
        ],
        rows=[],
    )

    indicador_carga = ft.ProgressRing(visible=False)
    texto_estado = ft.Text("Haga click aquí para cargar su archivo CSV o Excel.", color=ft.Colors.BLUE_GREY_400, text_align=ft.TextAlign.CENTER)

    def procesar_csv(file_path):
        """Procesa el CSV con el motor predictivo y actualiza la tabla."""
        file_name = os.path.basename(file_path)

        indicador_carga.visible = True
        texto_estado.value = "Entrenando modelo y generando predicciones. Por favor espere..."
        texto_estado.color = ft.Colors.BLUE_400
        page.update()

        try:
            motor = MotorInventario()
            df_crudo = pd.read_csv(file_path)
            df_limpio = motor.limpiar_datos(df_crudo)
            df_pred = motor.generar_prediccion(df_limpio, 15)

            stock_mock = {
                "Cerveza Pacifico": 50000,
                "Bloqueador Solar": 10,
                "Hielo en Bolsa": 0
            }
            df_alertas = motor.evaluar_stock(df_pred, stock_mock)

            nuevas_filas = []
            for _, row in df_alertas.iterrows():
                color = ft.Colors.RED_50 if row.get('Alerta_Surtir', False) else ft.Colors.GREEN_50
                alerta_icono = ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED) if row.get('Alerta_Surtir', False) else ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN)

                nuevas_filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row['Producto']))),
                            ft.DataCell(ft.Text(str(row['Venta_Estimada']))),
                            ft.DataCell(ft.Text(str(row['Stock_Actual']))),
                            ft.DataCell(ft.Text(str(row['Cantidad_A_Comprar']))),
                            ft.DataCell(alerta_icono)
                        ],
                        color=color
                    )
                )
            tabla_datos.rows = nuevas_filas
            texto_estado.value = f"Análisis completado para: {file_name}"
            texto_estado.color = ft.Colors.GREEN_600
        except Exception as ex:
            texto_estado.value = f"Error procesando el archivo: {str(ex)}"
            texto_estado.color = ft.Colors.RED_500

        indicador_carga.visible = False
        page.update()

    def abrir_dialogo_archivo():
        """Abre el explorador de archivos de Windows usando tkinter (nativo)."""
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de ventas",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")],
        )
        root.destroy()
        if file_path:
            procesar_csv(file_path)

    def abrirExploradorDeArchivos(e):
        threading.Thread(target=abrir_dialogo_archivo, daemon=True).start()

    boton_subir_csv = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.UPLOAD_FILE, size=40, color=ft.Colors.BLUE_GREY_400),
            ft.Text("Cargue sus datos de ventas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
            ft.Row([indicador_carga, texto_estado], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30,
        border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        on_click=abrirExploradorDeArchivos,
        ink=True
    )

    # Funciones de navegación
    def mostrar_panel(e):
        for control in sidebar_content.controls:
            if isinstance(control, ft.ListTile):
                control.selected = (control.title.value == "Panel de Control")
        contenedor_derecho.content = columna_principal
        page.update()

    def mostrar_reportes(e):
        for control in sidebar_content.controls:
            if isinstance(control, ft.ListTile):
                control.selected = (control.title.value == "Reportes")
        contenedor_derecho.content = crear_vista_reportes(page)
        page.update()

    # Menú Lateral (Sidebar)
    sidebar_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.BLUE_700, size=30),
                    ft.Text("Predictor", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
                ]),
                padding=ft.Padding(top=0, right=0, bottom=20, left=0)
            ),
            ft.Text("MENÚ PRINCIPAL", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_400),
            ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD), title=ft.Text("Panel de Control"), selected=True, on_click=mostrar_panel),
            ft.ListTile(leading=ft.Icon(ft.Icons.ANALYTICS), title=ft.Text("Reportes"), on_click=mostrar_reportes),
            ft.Divider(height=20),
            ft.Container(expand=True),
        ],
        spacing=5,
        expand=True
    )

    sidebar = ft.Container(
        content=sidebar_content,
        width=250,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius.only(top_right=15, bottom_right=15),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
    )

    # Contenido Principal
    header = ft.Container(
        content=ft.Text("Estación de Análisis Centralizada", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
        padding=ft.Padding(top=20, right=0, bottom=20, left=0)
    )

    tarjetas_superiores = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("Tendencia Histórica", weight=ft.FontWeight.BOLD),
                ft.Icon(ft.Icons.SHOW_CHART, size=50, color=ft.Colors.BLUE_500)
            ]),
            bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, expand=True, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Proyección de Ingresos", weight=ft.FontWeight.BOLD),
                ft.Icon(ft.Icons.BAR_CHART, size=50, color=ft.Colors.GREEN_500)
            ]),
            bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, expand=True, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
        )
    ], spacing=20)

    vista_datos = ft.Container(
        content=ft.Column([
            ft.Text("Resultados de Predicción", weight=ft.FontWeight.BOLD, size=18),
            ft.Row([tabla_datos], scroll=ft.ScrollMode.AUTO)
        ]),
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        margin=ft.Padding(top=20, right=0, bottom=0, left=0)
    )

    metricas_clave = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER_500), ft.Text("Métricas Clave & Resumen del Sistema", weight=ft.FontWeight.BOLD, size=18)]),
            ft.Text("Se han detectado patrones de crecimiento sostenido en la categoría SaaS. La proyección para el Q4 muestra un incremento del 15%."),
            ft.Divider(height=20),
            ft.Text("Recomendaciones:", weight=ft.FontWeight.BOLD),
            ft.Text("• Aumentar stock para SaaS Tier 1."),
            ft.Text("• Revisar precios de API Gateway.")
        ]),
        bgcolor=ft.Colors.BLUE_50, padding=20, border_radius=10,
        margin=ft.Padding(top=20, right=0, bottom=0, left=0)
    )

    columna_principal = ft.Column(
        controls=[
            header,
            ft.Text("Controles de Filtro", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_500),
            boton_subir_csv,
            ft.Container(height=10),
            tarjetas_superiores,
            vista_datos,
            metricas_clave
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    contenedor_derecho = ft.Container(content=columna_principal, padding=30, expand=True)

    cuerpo_dashboard = ft.Row(
        controls=[
            sidebar,
            contenedor_derecho
        ],
        expand=True,
        spacing=0
    )
    
    page.add(cuerpo_dashboard)

ft.run(main)