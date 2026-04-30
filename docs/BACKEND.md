s# Documentación del Backend - Inventario Predictivo

## Arquitectura General

El backend está organizado en módulos independientes que se ejecutan en secuencia:

```
Datos Crudos → Validador → Motor Predictivo → Reglas de Negocio → Exportación
```

---

## 1. ValidadorDatos (`validador.py`)

### Propósito
Recibir DataFrames crudos, validar integridad de datos, limpiar problemas y preparar para Prophet.

### Funcionalidades

#### `__init__()`
- Carga el histórico maestro desde `ArchivosCVS/historico_maestro.csv`
- Convierte columnas al formato Prophet: `ds` (fecha), `y` (ventas)

#### `validar_y_limpiar(df_crudo)`
Recibe un DataFrame con columnas `[Fecha, Producto, Ventas]` y retorna:

| Validación | Comportamiento |
|------------|----------------|
| Columnas requeridas | Lanza `ValueError` si faltan `Fecha`, `Producto` o `Ventas` |
| Valores nulos | Elimina filas con datos faltantes |
| Ventas numéricas | Convierte a número, filtra no numéricos |
| Ventas negativas | Lanza `ValueError` si existen valores < 0 |
| Fechas | Convierte a datetime, lanza error si falla |

**Concatenación con histórico:**
- Combina datos del usuario con el histórico maestro
- Elimina duplicados (mantiene datos del usuario sobre histórico)
- Retorna: `(df_unificado, df_usuario)`

---

## 2. MotorInventario (`predictor.py`)

### Propósito
Generar pronósticos de ventas utilizando Facebook Prophet.

### Atributos
- `df_historico`: DataFrame unificado con datos de ventas
- `feriados`: Días festivos de Mazatlán (Carnaval, Semana Santa)

### Funcionalidades

#### `generar_prediccion(start_date, end_date)`
Genera pronóstico para cada producto en el período especificado.

```
Parámetros:
  - start_date: Fecha inicio (str "YYYY-MM-DD")
  - end_date: Fecha fin (str "YYYY-MM-DD")

Retorna DataFrame:
  ┌──────────────┬──────────────────┐
  │ Producto     │ Venta_Estimada   │
  ├──────────────┼──────────────────┤
  │ Producto A   │ 150              │
  │ Producto B   │ 89               │
  └──────────────┴──────────────────┘
```

**Proceso por producto:**
1. Filtra datos históricos del producto
2. Entrena modelo Prophet con feriados de Mazatlán
3. Genera predicciones día a día
4. Suma totales del período

#### `calcular_metricas(dias_test=15)`
Evalúa precisión del modelo apartando datos para validación.

```
Parámetros:
  - dias_test: Cantidad de días para datos de prueba (default: 15)

Retorna DataFrame:
  ┌──────────────┬─────────┬─────────┐
  │ Producto     │ MAE     │ RMSE    │
  ├──────────────┼─────────┼─────────┤
  │ Producto A   │ 5.2     │ 7.8     │
  └──────────────┴─────────┴─────────┘

Métricas:
  - MAE (Mean Absolute Error): Error promedio absoluto
  - RMSE (Root Mean Square Error): Raíz del error cuadrático medio
```

---

## 3. LogicaNegocio (`reglas_negocio.py`)

### Propósito
Evaluar necesidades de reaprovisionamiento basadas en predicciones y stock actual.

### Funcionalidades

#### `evaluar_stock(df_predicciones, stock_actual_dict, porcentaje_seguridad=0)`
Compara ventas estimadas vs. inventario actual.

```
Parámetros:
  - df_predicciones: DataFrame con [Producto, Venta_Estimada]
  - stock_actual_dict: Dict {"Producto": cantidad_actual}
  - porcentaje_seguridad: Margen extra sobre estimado (default: 0)

Retorna DataFrame:
  ┌────────────┬───────────────┬─────────────┬─────────────────┬───────────────┐
  │ Producto   │ Venta_Estimada│ Stock_Actual│ Cantidad_A_Comprar│ Alerta_Surtir │
  ├────────────┼───────────────┼─────────────┼─────────────────┼───────────────┤
  │ Prod. A    │ 150           │ 100         │ 50              │ True          │
  │ Prod. B    │ 89            │ 120         │ 0               │ False         │
  └────────────┴───────────────┴─────────────┴─────────────────┴───────────────┘

Lógica:
  - stock_requerido = estimado * (1 + porcentaje_seguridad / 100)
  - Si stock_requerido > stock_actual → Alertar y calcular cantidad a comprar
```

---

## 4. ExportadorDatos (`exportador.py`)

### Propósito
Exportar DataFrames a archivos CSV para descarga.

### Funcionalidades

#### `__init__(ruta_default=None)`
- Define directorio de exportación (default: `Back/exports/`)
- Crea directorio si no existe

#### `exportar_a_csv(df, nombre_archivo="reporte_inventario.csv")`
```
Parámetros:
  - df: DataFrame a exportar
  - nombre_archivo: Nombre del archivo CSV

Retorna:
  - str: Ruta completa del archivo generado

Características:
  - Incluye BOM UTF-8 para compatibilidad con Excel
  - No incluye índice de DataFrame
```

---

## Flujo de Uso Integrado

```python
from Back.validador import ValidadorDatos
from Back.predictor import MotorInventario
from Back.reglas_negocio import LogicaNegocio
from Back.exportador import ExportadorDatos

# 1. Validar y unificar datos
validador = ValidadorDatos()
df_unificado, df_usuario = validador.validar_y_limpiar(df_crudo)

# 2. Generar predicciones
motor = MotorInventario(df_unificado)
predicciones = motor.generar_prediccion("2026-05-01", "2026-05-31")

# 3. Evaluar reglas de negocio
logica = LogicaNegocio()
alertas = logica.evaluar_stock(predicciones, stock_actual, porcentaje_seguridad=10)

# 4. Exportar resultados
exportador = ExportadorDatos()
ruta = exportador.exportar_a_csv(alertas, "alertas_mayo_2026")
```

---

## Formato de Datos

### Entrada esperada (DataFrame crudo)
| Columna   | Tipo   | Descripción                    |
|-----------|--------|--------------------------------|
| Fecha     | str    | Formato fecha (YYYY-MM-DD)     |
| Producto  | str    | Nombre/código del producto     |
| Ventas    | int/float | Cantidad vendida           |

### Formato interno (Prophet)
| Columna   | Tipo   | Descripción                    |
|-----------|--------|--------------------------------|
| ds        | date   | Fecha (Prophet format)         |
| y         | float  | Valor de ventas                |

---

## Notas de Implementación

1. **Feriados hardcodeados**: Los días festivos de Mazatlán están embebidos (Carnaval, Semana Santa)
2. **Concatenación con histórico**: Siempre se combina data nueva con el maestro para aprovechar datos previos
3. **Predicciones diarias**: Prophet genera predicciones día a día y luego se suman
4. **Márgenes de seguridad**: El usuario puede agregar un % extra sobre predicciones para conservatism