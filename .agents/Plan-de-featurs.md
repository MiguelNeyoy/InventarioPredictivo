Rol: Actúa como un Tech Lead especializado en Python, Pandas y arquitecturas de Inteligencia Artificial (Prophet).

Contexto del Sistema: Estoy desarrollando el backend de un "Gestor de Inventario Predictivo". Mi arquitectura actual se divide en módulos separados con Programación Orientada a Objetos:

validador.py: Limpia los datos y exige esquema (Fecha, Producto, Ventas/Cantidad).

predictor.py: Ejecuta el entrenamiento y predicción de series temporales producto por producto usando prophet.

reglas_negocio.py: Cruza la predicción con el stock físico y emite alertas booleanas.

generador.py: Crea el historico_maestro.csv con 3 años de datos simulados.

Objetivo:
Generar un plan de implementación técnico y directo (código listo para producción) para cubrir los 4 requerimientos críticos que faltan en el backend.

Requerimientos a implementar:

Concatenación Histórica en validador.py: Modificar el flujo para que lea el archivo local historico_maestro.csv, lo concatene (pd.concat) con el DataFrame crudo del usuario, elimine duplicados (drop_duplicates) manteniendo el más reciente, y pase el bloque completo a Prophet.

Evaluación Matemática (MAE y RMSE): Integrar scikit-learn para crear un método que evalúe el margen de error de la predicción ocultando los últimos 15 días reales del dataset y comparándolos con la predicción.

Umbrales Configurables en reglas_negocio.py: Modificar la lógica estricta (if estimado > stock_real) para aceptar un parámetro de "colchón de seguridad" (ej. disparar la alerta si el stock no cubre la demanda + 15% extra).

Módulo de Exportación: Crear la función para convertir el DataFrame resultante de reglas_negocio.py de vuelta a un archivo .csv descargable.

Formato de Salida Esperado:

Para cada requerimiento, indica exactamente en qué archivo y método se debe insertar el código.

Proporciona los bloques de código en Python optimizados y comentados.

Omite introducciones largas, conclusiones motivacionales o saludos. Ve directo al código y a la lógica de integración.