import sys
import os
import threading
import flet as ft
import pandas as pd
from datetime import date, timedelta

# Adicionando el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Back.validador import ValidadorDatos
from Back.predictor import MotorInventario
from Back.reglas_negocio import LogicaNegocio
from Back.exportador import ExportadorDatos
from reportes import crear_vista_reportes


# Variables globales para almacenar el último resultado
ultima_prediccion = None
ultima_metrica = None


def main(page: ft.Page):

    page.title = "Estación de Análisis Centralizada"
    page.bgcolor = "#F4F6F8"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280
    page.window_height = 800

    # Variables de estado
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

    # Métricas para reportes
    tabla_metricas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("MAE")),
            ft.DataColumn(ft.Text("RMSE")),
        ],
        rows=[],
    )

    indicador_carga = ft.ProgressRing(visible=False)
    texto_estado = ft.Text(
        "Configure los parámetros y cargue los archivos necesarios.",
        color=ft.Colors.BLUE_GREY_400,
        text_align=ft.TextAlign.CENTER,
    )

    # Controles de configuración
    campo_dias_prediccion = ft.TextField(
        label="Días a predecir",
        value="15",
        width=150,
        input_filter=ft.NumbersOnlyInputFilter(),
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

    # Variables para almacenar rutas de archivos
    ruta_archivo_ventas = ""
    ruta_archivo_stock = ""

    # Indicadores de archivos cargados
    texto_estado_ventas = ft.Text(
        "Archivo de ventas: No seleccionado", color=ft.Colors.GREY_600
    )
    texto_estado_stock = ft.Text(
        "Archivo de stock: No seleccionado", color=ft.Colors.GREY_600
    )

    def procesar_csv(file_path):
        """Procesa el CSV con el motor predictivo y actualiza la tabla."""
        file_name = os.path.basename(file_path)

        indicador_carga.visible = True
        texto_estado.value = (
            "Entrenando modelo y generando predicciones. Por favor espere..."
        )
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
                "Hielo en Bolsa": 0,
            }
            df_alertas = motor.evaluar_stock(df_pred, stock_mock)

            nuevas_filas = []
            for _, row in df_alertas.iterrows():
                color = (
                    ft.Colors.RED_50
                    if row.get("Alerta_Surtir", False)
                    else ft.Colors.GREEN_50
                )
                alerta_icono = (
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED)
                    if row.get("Alerta_Surtir", False)
                    else ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN)
                )

                nuevas_filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row["Producto"]))),
                            ft.DataCell(ft.Text(str(row["Venta_Estimada"]))),
                            ft.DataCell(ft.Text(str(row["Stock_Actual"]))),
                            ft.DataCell(ft.Text(str(row["Cantidad_A_Comprar"]))),
                            ft.DataCell(alerta_icono),
                        ],
                        color=color,
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

    def abrir_dialogo_ventas(e):
        """Abre el explorador de archivos para seleccionar ventas."""
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
            texto_estado_ventas.value = (
                f"Archivo de ventas: {os.path.basename(file_path)}"
            )
            texto_estado_ventas.color = ft.Colors.GREEN_600
            page.update()

    def abrir_dialogo_stock(e):
        """Abre el explorador de archivos para seleccionar stock."""
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
            texto_estado_stock.value = (
                f"Archivo de stock: {os.path.basename(file_path)}"
            )
            texto_estado_stock.color = ft.Colors.GREEN_600
            page.update()

    def procesar_prediccion(e):
        """Procesa la predicción con todos los parámetros configurados."""
        # Validar que se hayan seleccionado ambos archivos
        if not ruta_archivo_ventas:
            texto_estado.value = "Error: Debe seleccionar un archivo de ventas"
            texto_estado.color = ft.Colors.RED_500
            page.update()
            return

        if not ruta_archivo_stock:
            texto_estado.value = (
                "Error: Debe seleccionar un archivo de stock (obligatorio)"
            )
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

            # Ejecutar procesamiento en hilo separado para no bloquear UI
            threading.Thread(
                target=_procesar_prediccion_hilo,
                args=(ruta_archivo_ventas, ruta_archivo_stock, dias, umbral),
                daemon=True,
            ).start()
        except ValueError:
            texto_estado.value = "Error: Los días deben ser un número válido"
            texto_estado.color = ft.Colors.RED_500
            page.update()

    def _procesar_prediccion_hilo(
        ruta_ventas, ruta_stock, dias_prediccion, umbral_seguridad
    ):
        """Ejecuta el procesamiento en un hilo separado."""
        global ultima_prediccion, ultima_metrica

        try:
            indicador_carga.visible = True
            texto_estado.value = "Procesando predicción..."
            texto_estado.color = ft.Colors.BLUE_400
            page.update()

            # 1. Validar datos de ventas
            validador = ValidadorDatos()
            df_ventas = pd.read_csv(ruta_ventas)
            df_unificado, _ = validador.validar_y_limpiar(df_ventas)

            # 2. Cargar stock obligatorio
            df_stock = pd.read_csv(ruta_stock)
            # Validar que tenga las columnas requeridas
            if "Producto" not in df_stock.columns or "Stock" not in df_stock.columns:
                raise ValueError(
                    "El archivo de stock debe tener columnas 'Producto' y 'Stock'"
                )
            stock_dict = dict(zip(df_stock["Producto"], df_stock["Stock"]))

            # 3. Generar predicciones
            motor = MotorInventario(df_unificado)
            fecha_inicio = date.today()
            fecha_fin = fecha_inicio + timedelta(days=dias_prediccion)
            df_predicciones = motor.generar_prediccion(fecha_inicio, fecha_fin)

            # 4. Evaluar stock con umbral
            logica = LogicaNegocio()
            df_alertas = logica.evaluar_stock(
                df_predicciones, stock_dict, umbral_seguridad
            )

            # 5. Calcular métricas (últimos 15 días o menos si no hay suficientes datos)
            dias_test = min(
                15, len(df_unificado) // 2
            )  # Usar la mitad o 15, lo que sea menor
            if dias_test >= 5:  # Mínimo 5 días para métricas significativas
                df_metricas = motor.calcular_metricas(dias_test=dias_test)
            else:
                # Crear DataFrame vacío si no hay suficientes datos
                df_metricas = pd.DataFrame(columns=["Producto", "MAE", "RMSE"])

            # 6. Actualizar tabla de predicciones
            nuevas_filas = []
            for _, row in df_alertas.iterrows():
                color = (
                    ft.Colors.RED_50
                    if row.get("Alerta_Surtir", False)
                    else ft.Colors.GREEN_50
                )
                alerta_icono = (
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED)
                    if row.get("Alerta_Surtir", False)
                    else ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN)
                )

                nuevas_filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row["Producto"]))),
                            ft.DataCell(ft.Text(str(row["Venta_Estimada"]))),
                            ft.DataCell(ft.Text(str(row["Stock_Actual"]))),
                            ft.DataCell(ft.Text(str(row["Cantidad_A_Comprar"]))),
                            ft.DataCell(alerta_icono),
                        ],
                        color=color,
                    )
                )
            tabla_datos.rows = nuevas_filas

            # 7. Actualizar tabla de métricas
            filas_metricas = []
            for _, row in df_metricas.iterrows():
                filas_metricas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row["Producto"]))),
                            ft.DataCell(ft.Text(str(row["MAE"]))),
                            ft.DataCell(ft.Text(str(row["RMSE"]))),
                        ]
                    )
                )
            tabla_metricas.rows = filas_metricas

            # 8. Exportar a CSV
            exportador = ExportadorDatos()
            exportador.exportar_a_csv(df_alertas, "reporte_inventario.csv")

            # 9. Actualizar estado
            texto_estado.value = (
                f"Análisis completado para: {os.path.basename(ruta_ventas)}"
            )
            texto_estado.color = ft.Colors.GREEN_600

            # Guardar para reportes
            ultima_prediccion = df_alertas
            ultima_metrica = df_metricas

        except Exception as ex:
            texto_estado.value = f"Error procesando el archivo: {str(ex)}"
            texto_estado.color = ft.Colors.RED_500
        finally:
            indicador_carga.visible = False
            page.update()

    # Funciones de navegación
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
        contenedor_derecho.content = crear_vista_reportes(
            page, ultima_prediccion, ultima_metrica
        )
        page.update()

    # Menú Lateral (Sidebar)
    sidebar_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.BLUE_700, size=30),
                        ft.Text(
                            "Predictor",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ]
                ),
                padding=ft.Padding(top=0, right=0, bottom=20, left=0),
            ),
            ft.Text(
                "MENÚ PRINCIPAL",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_400,
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.DASHBOARD),
                title=ft.Text("Panel de Control"),
                selected=True,
                on_click=mostrar_panel,
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ANALYTICS),
                title=ft.Text("Reportes"),
                on_click=mostrar_reportes,
            ),
            ft.Divider(height=20),
            ft.Container(expand=True),
        ],
        spacing=5,
        expand=True,
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
        content=ft.Text(
            "Estación de Análisis Centralizada",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_GREY_900,
        ),
        padding=ft.Padding(top=20, right=0, bottom=20, left=0),
    )

    tarjetas_superiores = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
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
                    [
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
            [
                ft.Text("Resultados de Predicción", weight=ft.FontWeight.BOLD, size=18),
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
            [
                ft.Row(
                    [
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
            ft.Text(
                "Controles de Filtro",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_500,
            ),
            # Panel de configuración
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                campo_dias_prediccion,
                                ft.Text("días"),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                slider_umbral,
                                texto_umbral,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.UPLOAD_FILE),
                                            ft.Text("Cargar Archivo de Ventas"),
                                        ]
                                    ),
                                    on_click=abrir_dialogo_ventas,
                                ),
                                texto_estado_ventas,
                            ]
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.INVENTORY_2),
                                            ft.Text(
                                                "Cargar Archivo de Stock (OBLIGATORIO)"
                                            ),
                                        ]
                                    ),
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_600,
                                    on_click=abrir_dialogo_stock,
                                ),
                                texto_estado_stock,
                            ]
                        ),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.PLAY_ARROW),
                                    ft.Text("Procesar Predicción"),
                                ]
                            ),
                            icon=ft.Icons.PLAY_ARROW,
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            on_click=procesar_prediccion,
                            width=200,
                            height=40,
                        ),
                    ]
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
            ),
            ft.Container(height=10),
            tarjetas_superiores,
            vista_datos,
            metricas_clave,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    contenedor_derecho = ft.Container(
        content=columna_principal, padding=30, expand=True
    )

    cuerpo_dashboard = ft.Row(
        controls=[sidebar, contenedor_derecho], expand=True, spacing=0
    )

    page.add(cuerpo_dashboard)


ft.run(main)
