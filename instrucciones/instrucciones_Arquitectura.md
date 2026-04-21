# Instrucciones de Arquitectura Frontend: Dashboard Predictivo

Este documento define las reglas estrictas de desarrollo y la estructura obligatoria para la construcción de la interfaz gráfica en Flet. 

## 1. Reglas Innegociables de Arquitectura (Separación de Capas)
Para mantener el sistema modular y evitar corrupción de datos, el desarrollo del frontend debe adherirse a lo siguiente:

1. **Cero Lógica de Negocio en la UI:** El frontend tiene **estrictamente prohibido** calcular predicciones, sumar inventarios o definir si un producto requiere alerta. Su única función es "pintar" lo que el backend le entregue.
2. **El Contrato de Datos:** Toda la comunicación entre el backend y el frontend se hace mediante `pandas.DataFrame`. El componente visual recibe el DataFrame finalizado y simplemente lo itera.
3. **Estructura Modular Aislada:** No programar toda la interfaz en `app.py`. Cada bloque visual debe ser un componente independiente dentro de la carpeta `/components` e importarse en la vista principal.

## 2. Estructura de Directorios Obligatoria
Tu entorno de trabajo debe respetar este árbol:

```text
/Front
│── app.py                 # Inicializa Flet (page) y maneja el enrutamiento.
│── /views
│   └── dashboard.py       # Vista principal. Une los componentes y llama a las clases del backend.
└── /components
    ├── sidebar.py         # Menú lateral fijo.
    ├── upload_panel.py    # Contiene ft.FilePicker, ft.Slider (Umbral) y ft.ElevatedButton.
    ├── kpi_cards.py       # Renderiza el MAE y RMSE que entrega calcular_metricas().
    └── table_results.py   # Renderiza el plan de surtido. (Código provisto abajo).