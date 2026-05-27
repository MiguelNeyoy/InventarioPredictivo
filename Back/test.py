import os
import pandas as pd
from validador import ValidadorDatos
from predictor import MotorInventario
from reglas_negocio import LogicaNegocio

print("=== INICIANDO PRUEBA DEL FLUJO BACKEND MODULARIZADO ===\n")

# Cargar datos del mes actual
print("Cargando datos del mes actual...")
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", "ArchivosCSV", "ventas_mes_actual.csv")
    df_crudo = pd.read_csv(csv_path)
    if "Cantidad" in df_crudo.columns:
        df_crudo["Ventas"] = df_crudo["Cantidad"]  # Renombrar para consistencia si viene de origen anterior
    print("Datos del mes actual cargados correctamente.")
    print("Primeros registros:\n", df_crudo.head())
except Exception as e:
    print(f"Error al cargar ventas_mes_actual.csv: {e}")
    exit()

# 1. VALIDACION
print("\n--- Fase 1: Validación y Limpieza ---")
validador = ValidadorDatos()
try:
    df_unificado, df_usuario = validador.validar_y_limpiar(df_crudo)
    print("Formato de columnas ajustado para Prophet:")
    print(df_unificado.columns.tolist())
except ValueError as e:
    print(f"Error de validación: {e}")
    exit()

start_date = df_usuario["ds"].min().strftime("%Y-%m-%d")
end_date = df_usuario["ds"].max().strftime("%Y-%m-%d")
print(f"Periodo del mes actual: {start_date} a {end_date}")

# 2. PREDICCION
print("\n--- Fase 2: Motor Predictivo ---")
mi_motor = MotorInventario(df_unificado)
# Generar predicción para el periodo del mes actual
df_resultados = mi_motor.generar_prediccion(start_date, end_date)

# Calcular ventas reales por producto
ventas_reales = df_usuario.groupby("Producto")["y"].sum().reset_index()
ventas_reales = ventas_reales.rename(columns={"y": "Venta_Real"})
print("\nVentas reales del mes:")
print(ventas_reales)

print("\nVentas estimadas:")
print(df_resultados)

# Comparación
comparacion = pd.merge(df_resultados, ventas_reales, on="Producto", how="left")
comparacion["Diferencia"] = comparacion["Venta_Estimada"] - comparacion["Venta_Real"]
print("\nComparación Estimado vs Real:")
print(comparacion)

print("\n--- Métricas de Precisión (MAE / RMSE) ---")
_, df_metricas = mi_motor.generar_prediccion_y_metricas(start_date, end_date, dias_test=15)
print(df_metricas)

# Simulamos un diccionario de stock actual (lo que habría en la bodega hoy)
stock_falso = {
    "Cable de Red Cat6 3m": 500,
    "Pasta Térmica Arctic": 150,
    "Memoria USB 64GB": 200,
    "Memoria RAM 16GB DDR4": 8,
    "Disco Duro SSD 1TB": 6,
    "Monitor 24 Pulgadas": 2,
    "Tarjeta Gráfica RTX 4060": 5,
    "Laptop Gaming Asus": 4,
    "Laptop Dell Inspiron": 6,
    "Procesador Ryzen 5": 5,
}

# 3. REGLAS DE NEGOCIO
print("\n--- Fase 3: Evaluación de Inventario (Reglas de Negocio) ---")
logica = LogicaNegocio()
df_alertas = logica.evaluar_stock(df_resultados, stock_falso, porcentaje_seguridad=15)

print("\n=== RESULTADO FINAL QUE SE ENVIARÁ A FLET / FRONTEND === ")
# Imprimimos la tabla final bonita en la consola
print(df_alertas.to_string(index=False))

# 4. GRAFICAS POR DEFECTO DE PROPHET
print("\n--- Fase 4: Generando Gráfica por Defecto de Prophet ---")
try:
    from prophet import Prophet
    import matplotlib.pyplot as plt
    
    # Tomamos un producto de alta rotación para la demo gráfica
    producto_demo = "Cable de Red Cat6 3m"
    print(f"Generando gráfico nativo de Prophet para: {producto_demo}...")
    
    df_demo = df_unificado[df_unificado["Producto"] == producto_demo].copy()
    df_demo = df_demo.sort_values("ds")
    
    # Entrenar modelo demo
    modelo_demo = Prophet(holidays=mi_motor.feriados)
    modelo_demo.fit(df_demo[["ds", "y"]])
    
    # Crear periodo futuro extendido para que se aprecie la predicción
    futuro_demo = modelo_demo.make_future_dataframe(periods=30)
    prediccion_demo = modelo_demo.predict(futuro_demo)
    
    # Generar las figuras
    fig1 = modelo_demo.plot(prediccion_demo)
    plt.title(f"Predicción Nata de Prophet - {producto_demo}")
    
    fig2 = modelo_demo.plot_components(prediccion_demo)
    
    print("\n[INFO] Desplegando ventanas interactivas...")
    print("[INFO] Cierra las ventanas de los gráficos para terminar la ejecución del script.")
    plt.show()
    
except Exception as e:
    print(f"No se pudieron generar los gráficos por defecto de Prophet. Detalle: {e}")
