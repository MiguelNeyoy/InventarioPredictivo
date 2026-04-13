import pandas as pd
from validador import ValidadorDatos
from predictor import MotorInventario
from reglas_negocio import LogicaNegocio

print("=== INICIANDO PRUEBA DEL FLUJO BACKEND MODULARIZADO ===\n")

# Cargar datos del mes actual
print("Cargando datos del mes actual...")
try:
    df_crudo = pd.read_csv("ventas_mes_actual.csv")
    df_crudo["Ventas"] = df_crudo["Cantidad"]  # Renombrar para consistencia
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

# Simulamos un diccionario de stock actual (lo que habría en la bodega hoy)
stock_falso = {
    "Laptop Dell Inspiron": 50,
    "Procesador Ryzen 5": 20,
    "Memoria RAM 16GB": 100,
    "Tarjeta Gráfica RTX 4060": 10,
    "Monitor 24 pulgadas": 30,
}

# 3. REGLAS DE NEGOCIO
print("\n--- Fase 3: Evaluación de Inventario (Reglas de Negocio) ---")
logica = LogicaNegocio()
df_alertas = logica.evaluar_stock(df_resultados, stock_falso)

print("\n=== RESULTADO FINAL QUE SE ENVIARÁ A FLET / FRONTEND === ")
# Imprimimos la tabla final bonita en la consola
print(df_alertas.to_string(index=False))
