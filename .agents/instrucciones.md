# INSTRUCCIONES DE ARQUITECTURA: GESTOR DE INVENTARIO PREDICTIVO

## 1. Naturaleza y Reglas Base del Sistema
* **Patrón Arquitectónico:** Monolito Modular basado en Programación Orientada a Objetos (POO).
* **Comunicación:** NO SE USAN APIs (HTTP/REST) para evitar latencia. El Frontend importa las clases del Backend y ejecuta los procesos directamente en la memoria RAM.
* **Estructura de Datos Principal:** Todo el tránsito de información entre módulos se hace exclusivamente a través de DataFrames de `pandas`.
* **Esquema Estricto:** El modelo de datos transaccional depende innegociablemente de tres columnas: `Fecha`, `Producto` y `Cantidad`.

## 2. Mapa de Módulos (Separación de Responsabilidades)

El proyecto se divide estrictamente en dos capas. Ninguna capa debe asumir responsabilidades de la otra.

### Backend (`/Back`)
1. `validador.py` (Clase `ValidadorDatos`): 
   - **Única función:** Recibir CSV crudo, concatenar con `historico_maestro.csv`, purgar nulos, renombrar columnas para Prophet (`ds`, `y`) y validar estructura. 
   - **Regla:** Si los datos fallan, levanta una excepción (`raise ValueError`), nunca intenta adivinar datos.
2. `predictor.py` (Clase `MotorInventario`): 
   - **Única función:** Ejecutar algoritmos matemáticos. Aplica estacionalidad (feriados locales), aísla productos mediante bucles, entrena `prophet` (`.fit()`) y calcula métricas de error (MAE/RMSE) con `scikit-learn`.
3. `reglas_negocio.py` (Clase `LogicaNegocio`): 
   - **Única función:** Cruzar DataFrames. Resta la predicción matemática contra el stock real en bodega y aplica umbrales de seguridad para emitir la columna booleana `Alerta_Surtir`.

### Frontend (`/Front/src`)
1. `app.py` y componentes Flet:
   - **Única función:** Interfaz gráfica (SPA). Se divide en componentes: Layout (Sidebar/Header), Inputs (`FilePicker`), Gráficos (Plotly/Matplotlib inyectado) y Tablas (`DataTable`).
   - **Regla de Estado:** La UI reacciona a los DataFrames devueltos por el Backend.

## 3. Protocolo Estricto para la Creación de Nuevas Features

Toda nueva funcionalidad debe desarrollarse siguiendo este orden secuencial. Prohibido programar la interfaz visual antes de tener la estructura de datos resuelta.

### Paso 1: Actualizar el Modelo de Datos (Validador)
* ¿La nueva feature requiere leer un dato nuevo (ej. "Precio" o "Categoría")?
* Actualizar el esquema aceptado en `validador.py`.
* Asegurar que la concatenación de datos soporte la nueva columna sin inyectar `NaNs`.

### Paso 2: Lógica Matemática o de Negocio (Backend)
* ¿Es un cálculo estadístico? Va en `predictor.py`.
* ¿Es una regla humana o de administración? Va en `reglas_negocio.py`.
* La función debe recibir un DataFrame, transformarlo y **retornar un DataFrame**. No debe imprimir a consola (excepto logs) ni interactuar con la UI.

### Paso 3: Puente de Integración
* Importar el método actualizado en el controlador principal del Frontend (`procesar_archivo` en `app.py`).
* Probar el flujo pasando variables "Mock" si es necesario aislar el comportamiento.

### Paso 4: Renderizado en Frontend (Flet)
* Usar el DataFrame resultante para actualizar la UI.
* Mapear iterativamente (bucles `for`) las filas del DataFrame hacia componentes nativos (`ft.DataRow`, `ft.Card`).
* Actualizar el estado ejecutando `page.update()`.

## 4. Reglas Críticas de Flet (Manejo de Errores Comunes)
* **FilePicker:** Debe instanciarse y agregarse al `page.overlay` una única vez al iniciar la aplicación, fuera de las funciones de clic, para evitar errores de *Timeout* o *Unknown Control*.
* **Concurrencia:** Evitar el uso de `async/await` a menos que sea estrictamente necesario para operaciones I/O externas. Las predicciones bloquean el hilo principal por diseño.
* **Componentes Dinámicos:** Las tablas y gráficas deben instanciarse vacías y actualizar sus propiedades (`rows`, `controls`) posteriormente durante la ejecución de los métodos del backend.