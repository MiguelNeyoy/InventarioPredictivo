# InventarioPredictivo

Sistema de gestión de inventario con capacidades de predicción de ventas para el sector retail/minorista.

## Descripción

Utiliza modelos de series temporales (Prophet) para forecasting de demanda, permitiendo optimizar niveles de stock y reducir faltantes o excesos de inventario.

## Características

- **Predicción de ventas**: Forecasting diario/semanal/mensual por producto
- **Alertas automáticas**: Notificaciones de productos que requieren reaprovisionamiento
- **Validación de datos**: Limpieza y normalización de datos históricos
- **Métricas de precisión**: MAE y RMSE para evaluar calidad del modelo
- **Exportación flexible**: Descarga de reportes en formato CSV
- **Feriados regionales**: Calendario configurable para mayor precisión en predicciones

## Requisitos

- Python 3.10+
- pandas
- prophet
- scikit-learn
- flet

## Estructura del Proyecto

```
InventarioPredictivo/
├── Back/
│   ├── validador.py      # Validación y limpieza de datos
│   ├── predictor.py      # Motor de predicciones
│   ├── reglas_negocio.py # Lógica de alertas de stock
│   └── exportador.py     # Exportación a CSV
├── Frontend/
│   └── src/
│       └── app.py        # Aplicación Flet
├── ArchivosCVS/          # Datos históricos
└── docs/                 # Documentación técnica
```

## Instalación

```bash
pip install pandas prophet scikit-learn flet
```

## Uso

1. Importa los módulos del backend en tu aplicación
2. Carga datos de ventas con columnas: `Fecha`, `Producto`, `Ventas`
3. Ejecuta el pipeline:

```python
from Back.validador import ValidadorDatos
from Back.predictor import MotorInventario
from Back.reglas_negocio import LogicaNegocio

# Validar datos
validador = ValidadorDatos()
df_unificado, _ = validador.validar_y_limpiar(df_crudo)

# Generar predicciones
motor = MotorInventario(df_unificado)
predicciones = motor.generar_prediccion("2026-05-01", "2026-05-31")

# Evaluar stock
logica = LogicaNegocio()
alertas = logica.evaluar_stock(predicciones, stock_actual)
```

4. Inicia la interfaz:

```bash
python Frontend/src/app.py
```

## Formato de Datos

### Entrada (CSV)
| Fecha       | Producto | Ventas |
|-------------|----------|--------|
| 2026-01-01  | Prod-A   | 150    |
| 2026-01-02  | Prod-A   | 142    |

### Columnas requeridas
- `Fecha`: Formato YYYY-MM-DD
- `Producto`: Identificador del artículo
- `Ventas`: Cantidad vendida (entero positivo)

## Métricas del Modelo

- **MAE** (Mean Absolute Error): Error promedio absoluto
- **RMSE** (Root Mean Square Error): Raíz del error cuadrático medio

Valores más bajos indican mejor precisión del modelo.

## Licencia

MIT