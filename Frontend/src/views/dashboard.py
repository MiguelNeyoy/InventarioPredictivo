import sys
import os
import threading
import flet as ft
import pandas as pd
from datetime import date, timedelta

_back_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Back"))
if _back_path not in sys.path:
    sys.path.insert(0, _back_path)

from validador import ValidadorDatos
from predictor import MotorInventario
from reglas_negocio import LogicaNegocio
from exportador import ExportadorDatos

from components.sidebar import crear_sidebar
from components.upload_panel import crear_upload_panel
from components.kpi_cards import crear_kpi_cards
from components.table_results import crear_tabla_resultados


ultima_prediccion = None
ultima_metrica = None
ruta_archivo_ventas = ""
ruta_archivo_stock = ""


def crear_vista_dashboard(page: ft.Page):
    global ultima_prediccion, ultima_metrica, ruta_archivo_ventas, ruta_archivo_stock

    indicador_carga = ft.ProgressRing(visible=False, scale=1.5)
    texto_estado = ft.Text(
        "Configure los parámetros y cargue los archivos necesarios.",
        color=ft.Colors.BLUE_GREY_400,
        text_align=ft.TextAlign.CENTER,
    )

    campo_dias_prediccion = ft.TextField(
        label="Días a predecir", value="15", width=150, input_filter=ft.NumbersOnlyInputFilter()
    )
    slider_umbral = ft.Slider(
        min=0,
        max=50,
        divisions=10,
        label="{value}%",
        value=0,
        width=200,
    )
    texto_umbral = ft.Text("Umbral de seguridad: 0%")

    texto_estado_ventas = ft.Text(
        "Archivo de ventas: No seleccionado", color=ft.Colors.GREY_600
    )
    texto_estado_stock = ft.Text(
        "Archivo de stock: No seleccionado", color=ft.Colors.GREY_600
    )

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Venta Estimada")),
            ft.DataColumn(ft.Text("Stock Actual")),
            ft.DataColumn(ft.Text("Cant. Comprar")),
            ft.DataColumn(ft.Text("Alerta")),
        ],
        rows=[],
    )

    kpi_container = ft.Row(
        controls=[],
        spacing=20,
    )

    def actualizar_tabla(df_alertas):
        nuevas_filas = []
        for _, row in df_alertas.iterrows():
            alerta = row.get("Alerta_Surtir", False)
            color = ft.Colors.RED_50 if alerta else ft.Colors.GREEN_50
            alerta_icono = (
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED)
                if alerta
                else ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN)
            )
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row.get("Producto", "")))),
                        ft.DataCell(ft.Text(str(row.get("Venta_Estimada", 0)))),
                        ft.DataCell(ft.Text(str(row.get("Stock_Actual", 0)))),
                        ft.DataCell(ft.Text(str(row.get("Cantidad_A_Comprar", 0)))),
                        ft.DataCell(alerta_icono),
                    ],
                    color=color,
                )
            )
        tabla_datos.rows = nuevas_filas

    def abrir_dialogo_ventas(e):
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
            global ruta_archivo_ventas
            ruta_archivo_ventas = file_path
            texto_estado_ventas.value = f"Archivo de ventas: {os.path.basename(file_path)}"
            texto_estado_ventas.color = ft.Colors.GREEN_600
            page.update()

    def abrir_dialogo_stock(e):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de stock",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")],
        )
        root.destroy()
        if file_path:
            global ruta_archivo_stock
            ruta_archivo_stock = file_path
            texto_estado_stock.value = f"Archivo de stock: {os.path.basename(file_path)}"
            texto_estado_stock.color = ft.Colors.GREEN_600
            page.update()

    def procesar_prediccion(e):
        if not ruta_archivo_ventas:
            texto_estado.value = "Error: Debe seleccionar un archivo de ventas"
            texto_estado.color = ft.Colors.RED_500
            page.update()
            return

        if not ruta_archivo_stock:
            texto_estado.value = "Error: Debe seleccionar un archivo de stock (obligatorio)"
            texto_estado.color = ft.Colors.RED_500
            page.update()
            return

        try:
            dias = int(campo_dias_prediccion.value)
            if dias <= 0 or dias > 365:
                texto_estado.value = "Error: Los días deben estar entre 1 y 365"
                texto_estado.color = ft.Colors.RED_500
                page.update()
                return

            umbral = slider_umbral.value
            threading.Thread(
                target=_procesar_prediccion_hilo,
                args=(ruta_archivo_ventas, ruta_archivo_stock, dias, umbral),
                daemon=True,
            ).start()
        except ValueError:
            texto_estado.value = "Error: Los días deben ser un número válido"
            texto_estado.color = ft.Colors.RED_500
            page.update()

    def _procesar_prediccion_hilo(ruta_ventas, ruta_stock, dias_prediccion, umbral_seguridad):
        global ultima_prediccion, ultima_metrica
        print(f"[DEBUG] Processing with ventas: {ruta_ventas}, stock: {ruta_stock}")

        try:
            indicador_carga.visible = True
            indicador_carga.scale = 2
            texto_estado.value = "Entrenando modelo y generando predicciones..."
            texto_estado.color = ft.Colors.BLUE_400
            page.update()

            validador = ValidadorDatos()
            df_ventas = pd.read_csv(ruta_ventas)
            print(f"[DEBUG] Ventas columns: {list(df_ventas.columns)}")
            df_unificado, _ = validador.validar_y_limpiar(df_ventas)

            df_stock = pd.read_csv(ruta_stock)
            print(f"[DEBUG] Stock columns: {list(df_stock.columns)}")
            stock_col = "Stock" if "Stock" in df_stock.columns else "Stock_Actual"
            if "Producto" not in df_stock.columns or stock_col not in df_stock.columns:
                raise ValueError(f"El archivo de stock debe tener columnas 'Producto' y '{stock_col}'")
            stock_dict = dict(zip(df_stock["Producto"], df_stock[stock_col]))

            motor = MotorInventario(df_unificado)
            fecha_inicio = date.today()
            fecha_fin = fecha_inicio + timedelta(days=dias_prediccion)
            df_predicciones = motor.generar_prediccion(fecha_inicio, fecha_fin)

            logica = LogicaNegocio()
            df_alertas = logica.evaluar_stock(df_predicciones, stock_dict, umbral_seguridad)

            dias_test = min(15, len(df_unificado) // 2)
            if dias_test >= 5:
                df_metricas = motor.calcular_metricas(dias_test=dias_test)
            else:
                df_metricas = pd.DataFrame(columns=["Producto", "MAE", "RMSE"])

            actualizar_tabla(df_alertas)

            kpi_container.controls = crear_kpi_cards(df_metricas).controls

            exportador = ExportadorDatos()
            exportador.exportar_a_csv(df_alertas, "reporte_inventario.csv")

            ultima_prediccion = df_alertas
            ultima_metrica = df_metricas

            texto_estado.value = f"Análisis completado exitosamente"
            texto_estado.color = ft.Colors.GREEN_600

        except Exception as ex:
            texto_estado.value = f"Error procesando el archivo: {str(ex)}"
            texto_estado.color = ft.Colors.RED_500
            page.update()
        finally:
            indicador_carga.visible = False
            page.update()

    def mostrar_panel(e):
        for control in sidebar_content.controls:
            if isinstance(control, ft.ListTile):
                control.selected = control.title.value == "Panel de Control"
        contenedor_derecho.content = columna_principal
        page.update()

    def mostrar_reportes(e):
        for control in sidebar_content.controls:
            if isinstance(control, ft.ListTile):
                control.selected = control.title.value == "Reportes"
        from reportes import crear_vista_reportes
        contenedor_derecho.content = crear_vista_reportes(page, ultima_prediccion, ultima_metrica)
        page.update()

    sidebar = crear_sidebar(page, mostrar_panel, mostrar_reportes)

    sidebar_content = sidebar.content

    upload = crear_upload_panel(
        campo_dias_prediccion,
        slider_umbral,
        texto_umbral,
        texto_estado_ventas,
        texto_estado_stock,
        abrir_dialogo_ventas,
        abrir_dialogo_stock,
        procesar_prediccion,
    )

    header = ft.Container(
        content=ft.Text(
            "Estación de Análisis Centralizada",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_GREY_900,
        ),
        padding=ft.Padding(top=20, right=0, bottom=20, left=0),
    )

    tarjetas_superiores = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Tendencia Histórica", weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.SHOW_CHART, size=50, color=ft.Colors.BLUE_500),
                    ]
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Proyección de Ingresos", weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.BAR_CHART, size=50, color=ft.Colors.GREEN_500),
                    ]
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
        ],
        spacing=20,
    )

    vista_datos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Resultados de Predicción", weight=ft.FontWeight.BOLD, size=18
                ),
                ft.Row([tabla_datos], scroll=ft.ScrollMode.AUTO),
            ]
        ),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        margin=ft.Padding(top=20, right=0, bottom=0, left=0),
    )

    metricas_clave = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER_500),
                        ft.Text(
                            "Métricas Clave & Resumen del Sistema",
                            weight=ft.FontWeight.BOLD,
                            size=18,
                        ),
                    ]
                ),
                ft.Text(
                    "Se han detectado patrones de crecimiento sostenido en la categoría SaaS. La proyección para el Q4 muestra un incremento del 15%."
                ),
                ft.Divider(height=20),
                ft.Text("Recomendaciones:", weight=ft.FontWeight.BOLD),
                ft.Text("• Aumentar stock para SaaS Tier 1."),
                ft.Text("• Revisar precios de API Gateway."),
            ]
        ),
        bgcolor=ft.Colors.BLUE_50,
        padding=20,
        border_radius=10,
        margin=ft.Padding(top=20, right=0, bottom=0, left=0),
    )

    columna_principal = ft.Column(
        controls=[
            header,
            upload,
            ft.Container(height=10),
            kpi_container,
            tarjetas_superiores,
            vista_datos,
            metricas_clave,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    kpi_container.controls = crear_kpi_cards().controls

    contenedor_derecho = ft.Container(content=columna_principal, padding=30, expand=True)

    cuerpo_dashboard = ft.Row(
        controls=[sidebar, contenedor_derecho], expand=True, spacing=0
    )

    return ft.Column(
        controls=[indicador_carga, texto_estado, cuerpo_dashboard],
        expand=True,
        spacing=0,
    )