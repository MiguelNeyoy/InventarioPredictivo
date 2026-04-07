import pandas as pd
from validador import ValidadorDatos
from predictor import MotorInventario
from reglas_negocio import LogicaNegocio

print("=== INICIANDO PRUEBA DEL FLUJO BACKEND MODULARIZADO ===\n")

# Simulamos lo que haría el controlador (por ejemplo FastApi o Flask) o Frontend
try:
    df_crudo = pd.read_csv("ventas_totales.csv")
    print("Archivo CSV cargado correctamente (Simulación de entrada cruda).")
except FileNotFoundError:
    print("Error: No encuentro el CSV.")
    exit()

# 1. VALIDACION
print("\n--- Fase 1: Validación y Limpieza ---")
validador = ValidadorDatos()
try:
    df_limpio = validador.validar_y_limpiar(df_crudo)
    print("Formato de columnas ajustado para Prophet:")
    print(df_limpio.columns.tolist()) 
except ValueError as e:
    print(f"Error de validación: {e}")
    exit()

# 2. PREDICCION
print("\n--- Fase 2: Motor Predictivo ---")
mi_motor = MotorInventario()
# Le pedimos predecir 15 días. Esto tomará unos segundos porque entrenará la IA.
df_resultados = mi_motor.generar_prediccion(df_limpio, dias_a_predecir=15)

# Simulamos un diccionario de stock actual (lo que habría en la bodega hoy)
stock_falso = {
    "Cerveza Pacifico": 50000,  # Tenemos mucha, no debería pedir
    "Bloqueador Solar": 10,     # Tenemos poco, debería alertar
    "Hielo en Bolsa": 0         # No tenemos nada, alerta crítica
}

# 3. REGLAS DE NEGOCIO
print("\n--- Fase 3: Evaluación de Inventario (Reglas de Negocio) ---")
logica = LogicaNegocio()
df_alertas = logica.evaluar_stock(df_resultados, stock_falso)

print("\n=== RESULTADO FINAL QUE SE ENVIARÁ A FLET / FRONTEND === ")
# Imprimimos la tabla final bonita en la consola
print(df_alertas.to_string(index=False))