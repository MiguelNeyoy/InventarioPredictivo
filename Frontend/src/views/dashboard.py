import sys
import os
import flet as ft
import pandas as pd
from datetime import date, timedelta
import asyncio

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
from components.chart_line import crear_grafico_linea
from components.chart_bar import crear_grafico_barras, crear_top_productos_chart


class AppState:
    def __init__(self):
        self.predicciones = None
        self.metricas = None
        self.df_historico = None
        self.ruta_archivo_ventas = ""
        self.ruta_archivo_stock = ""
        self.procesando = False


app_state = AppState()


def crear_vista_dashboard(page: ft.Page):
    global app_state

    indicador_carga = ft.ProgressRing(visible=False, scale=1.5)
    texto_estado = ft.Text(
        "Configure los parámetros y cargue los archivos necesarios.",
        color=ft.Colors.BLUE_GREY_400,
        text_align=ft.TextAlign.CENTER,
    )
    banner_error = ft.Banner(
        bgcolor=ft.Colors.RED_100,
        content=ft.Text("", color=ft.Colors.RED_900),
        actions=[ft.TextButton("CERRAR", on_click=lambda e: cerrar_banner())],
    )

    def cerrar_banner():
        banner_error.visible = False
        page.update()

    def mostrar_error(mensaje):
        banner_error.content = ft.Text(mensaje)
        banner_error.visible = True
        page.update()

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
    texto_umbral_label = ft.Text("Umbral de seguridad: 0%")

    def actualizar_label_umbral(e):
        valor = int(slider_umbral.value)
        texto_umbral_label.value = f"Umbral de seguridad: {valor}%"
        page.update()

    slider_umbral.on_change = actualizar_label_umbral

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

    grafico_tendencia = None
    grafico_barras = None

    def actualizar_graficos():
        nonlocal grafico_tendencia, grafico_barras
        grafico_tendencia = crear_grafico_linea(app_state.df_historico, app_state.predicciones, "Tendencia Histórica")
        grafico_barras = crear_grafico_barras(app_state.predicciones, "Ventas por Producto")
        return grafico_tendencia, grafico_barras

    graf_tendencia, graf_barras = actualizar_graficos()

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def on_file_ventas_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            app_state.ruta_archivo_ventas = e.files[0].path
            texto_estado_ventas.value = f"Archivo de ventas: {e.files[0].name}"
            texto_estado_ventas.color = ft.Colors.GREEN_600
        page.update()

    def on_file_stock_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            app_state.ruta_archivo_stock = e.files[0].path
            texto_estado_stock.value = f"Archivo de stock: {e.files[0].name}"
            texto_estado_stock.color = ft.Colors.GREEN_600
        page.update()

    file_picker.on_result = lambda e: (
        on_file_ventas_result(e) if hasattr(e, 'files') and app_state.ruta_archivo_stock == "" 
        else on_file_stock_result(e)
    )

    def abrir_dialogo_ventas(e):
        file_picker.pick_files(
            allowed=["csv", "xlsx"],
            dialog_title="Seleccionar archivo de ventas",
            on_result=on_file_ventas_result
        )

    def abrir_dialogo_stock(e):
        file_picker.pick_files(
            allowed=["csv", "xlsx"],
            dialog_title="Seleccionar archivo de stock",
            on_result=on_file_stock_result
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

    async def procesar_prediccion(e):
        if not app_state.ruta_archivo_ventas:
            mostrar_error("Debe seleccionar un archivo de ventas")
            return

        if not app_state.ruta_archivo_stock:
            mostrar_error("Debe seleccionar un archivo de stock (obligatorio)")
            return

        try:
            dias = int(campo_dias_prediccion.value)
            if dias <= 0 or dias > 365:
                mostrar_error("Los días deben estar entre 1 y 365")
                return
        except ValueError:
            mostrar_error("Los días deben ser un número válido")
            return

        indicador_carga.visible = True
        indicador_carga.scale = 2
        texto_estado.value = "Entrenando modelo y generando predicciones..."
        texto_estado.color = ft.Colors.BLUE_400
        page.update()

        try:
            df_alertas, df_metricas, df_hist = await asyncio.to_thread(
                _procesar_prediccion_sync,
                app_state.ruta_archivo_ventas,
                app_state.ruta_archivo_stock,
                dias,
                slider_umbral.value
            )

            app_state.predicciones = df_alertas
            app_state.metricas = df_metricas
            app_state.df_historico = df_hist

            actualizar_tabla(df_alertas)
            kpi_container.controls = crear_kpi_cards(df_metricas).controls

            nuevo_tendencia = crear_grafico_linea(df_hist, df_alertas, "Tendencia Histórica")
            nuevo_barras = crear_grafico_barras(df_alertas, "Ventas por Producto")
            
            tarjetas_superiores.controls = [nuevo_tendencia, nuevo_barras]

            indicador_carga.visible = False
            texto_estado.value = "Análisis completado exitosamente"
            texto_estado.color = ft.Colors.GREEN_600

        except Exception as ex:
            indicador_carga.visible = False
            mostrar_error(f"Error procesando: {str(ex)}")
            texto_estado.value = "Error en el procesamiento"
            texto_estado.color = ft.Colors.RED_500

        page.update()

    def _procesar_prediccion_sync(ruta_ventas, ruta_stock, dias_prediccion, umbral_seguridad):
        validador = ValidadorDatos()
        df_ventas = pd.read_csv(ruta_ventas)
        df_unificado, df_usuario = validador.validar_y_limpiar(df_ventas)

        df_stock = pd.read_csv(ruta_stock)
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

        exportador = ExportadorDatos()
        exportador.exportar_a_csv(df_alertas, "reporte_inventario.csv")

        return df_alertas, df_metricas, df_unificado

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
        contenedor_derecho.content = crear_vista_reportes(
            page, 
            app_state.predicciones, 
            app_state.metricas,
            app_state.df_historico
        )
        page.update()

    sidebar = crear_sidebar(page, mostrar_panel, mostrar_reportes)
    sidebar_content = sidebar.content

    upload = crear_upload_panel(
        campo_dias_prediccion,
        slider_umbral,
        texto_umbral_label,
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
            crear_grafico_linea(app_state.df_historico, app_state.predicciones, "Tendencia Histórica"),
            crear_grafico_barras(app_state.predicciones, "Ventas por Producto"),
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
        controls=[banner_error, indicador_carga, texto_estado, cuerpo_dashboard],
        expand=True,
        spacing=0,
    )