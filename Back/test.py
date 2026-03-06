import pandas as pd
from predictor import MotorInventario # Importamos la clase

print("=== INICIANDO PRUEBA DEL MOTOR BACKEND ===\n")

# 1. Simulamos lo que haría el compañero del Frontend (Leer el archivo)
try:
    df_crudo = pd.read_csv("ventas_totales.csv")
    print("Archivo CSV cargado correctamente (Simulación de Frontend).")
except FileNotFoundError:
    print("Error: No encuentro el CSV.")
    exit()

# 2. Creamos el objeto de tu clase
mi_motor = MotorInventario()

# 3. Probamos el método de limpieza
print("\n--- Probando limpiar_datos() ---")
df_limpio = mi_motor.limpiar_datos(df_crudo)
print("Formato de columnas ajustado para Prophet:")
print(df_limpio.columns.tolist()) # Debería imprimir ['ds', 'Producto', 'y']

# 4. Probamos el método fuerte: La Predicción
print("\n--- Probando generar_prediccion() ---")
# Le pedimos predecir 15 días. Esto tomará unos segundos porque entrenará la IA.
df_resultados = mi_motor.generar_prediccion(df_limpio, dias_a_predecir=15)

# 5. Simulamos un diccionario de stock actual (lo que habría en la bodega hoy)
stock_falso = {
    "Cerveza Pacifico": 50000,  # Tenemos mucha, no debería pedir
    "Bloqueador Solar": 10,   # Tenemos poco, debería alertar
    "Hielo en Bolsa": 0       # No tenemos nada, alerta crítica
}

# 6. Probamos el motor de reglas de negocio
print("\n--- Probando evaluar_stock() ---")
df_alertas = mi_motor.evaluar_stock(df_resultados, stock_falso)

print("\n=== RESULTADO FINAL QUE SE ENVIARÁ A FLET === ")
# Imprimimos la tabla final bonita en la consola
print(df_alertas.to_string(index=False))