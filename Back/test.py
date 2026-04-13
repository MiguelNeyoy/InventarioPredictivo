import pandas as pd
from validador import ValidadorDatos
from predictor import MotorInventario
from reglas_negocio import LogicaNegocio

print("=== INICIANDO PRUEBA DEL FLUJO BACKEND MODULARIZADO ===\n")

# 0. CARGA DE DATOS
print("\n--- Fase 0: Cargando datos del histórico ---")
df_crudo = pd.read_csv('historico_maestro.csv')
print(f"✓ Datos cargados: {len(df_crudo)} registros")
print(f"Columnas: {df_crudo.columns.tolist()}")

# Para las pruebas, utilizaremos un stock falso
stock_falso = 10

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

# 3. REGLAS DE NEGOCIO
print("\n--- Fase 3: Evaluación de Inventario (Reglas de Negocio) ---")
logica = LogicaNegocio()
df_alertas = logica.evaluar_stock(df_resultados, stock_falso)

print("\n=== RESULTADO FINAL QUE SE ENVIARÁ A FLET / FRONTEND === ")
# Imprimimos la tabla final bonita en la consola
print(df_alertas.to_string(index=False))