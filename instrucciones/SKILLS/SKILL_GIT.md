# SKILL: Estándares de Commits y Entregas Atómicas

Para mantener el historial del proyecto limpio, rastreable y profesional, todo el equipo debe adherirse estrictamente a las siguientes reglas al registrar sus cambios en Git. Un historial desordenado retrasa el paso a producción y dificulta encontrar el origen de los errores.

## 1. Nomenclatura de Prefijos (El "Qué")
Cada commit debe empezar obligatoriamente con uno de los siguientes prefijos en mayúsculas, seguido de dos puntos y un espacio. Esto permite filtrar rápidamente el historial.

* **FEATURE:** Para nuevas funcionalidades o características que agregan valor al producto (Ej. Nuevas vistas, nuevos endpoints, integración de APIs).
* **FIX:** Para la resolución de un bug o error en el código existente.
* **REFACTOR:** Para cambios en el código que no corrigen un bug ni añaden una funcionalidad, pero mejoran la estructura, legibilidad o rendimiento (Ej. Extraer un componente Blade, optimizar un query).
* **CHORE:** Para tareas de mantenimiento que no afectan el código de producción (Ej. Actualizar dependencias de Composer/NPM, cambios en `.gitignore`, configuración de base de datos).
* **DOCS:** Para cambios exclusivos en la documentación (Ej. Actualizar el README, agregar un archivo de diseño).

*Ejemplo de título correcto:* `FEATURE: Agrega botón de contacto por WhatsApp en detalle de terreno`

## 2. La Regla de Oro: Commits Atómicos
Un commit atómico significa que **un commit representa una sola unidad lógica de trabajo**. 

**Reglas de atomicidad:**
1. **Un problema = Un commit:** Si tu commit dice "Agrega login Y arregla el color del footer", tu commit no es atómico. Deben ser dos commits distintos (`FEATURE` para el login, `FIX` para el footer).
2. **Debe compilar/funcionar:** Un commit nunca debe romper el sistema. Si descargo exactamente ese commit, la aplicación debe poder ejecutarse sin errores fatales.
3. **Cambios agrupados:** Si creaste una migración, el modelo de Eloquent y el controlador para los "Apartados", esos archivos deben ir en el mismo commit porque son parte de la misma unidad lógica.

## 3. Redacción del Mensaje: Contexto y el "Por Qué"
El título del commit dice *qué* hace el código, pero el cuerpo del mensaje debe explicar *por qué* se hizo y dar antecedentes. El código ya nos dice cómo lo hiciste; el mensaje debe decirnos la razón de negocio o técnica.

**Estructura obligatoria:**
1. **Título (Subject):** Máximo 50 caracteres. Usa modo imperativo (como si estuvieras dando una orden: "Agrega", "Corrige", "Elimina", no "Agregando" o "Agregado").
2. **Línea en blanco:** Obligatoria para separar el título del cuerpo.
3. **Cuerpo (Body):**
   * **Antecedentes:** ¿Cuál era el problema o estado anterior?
   * **Solución/Por qué:** ¿Por qué se eligió esta solución? Menciona si afecta a otras partes del sistema o si hay consideraciones a tomar en cuenta.

## 4. Ejemplo Perfecto de un Commit

```text
FIX: Corrige error de validación en el formulario de terrenos

Antecedentes:
Actualmente, si un usuario subía un precio mayor a 10 millones, 
la base de datos MariaDB arrojaba un error 500 porque el campo 
estaba definido como entero estándar.

Solución:
Se actualizó el `StoreLandRequest` para limitar el input a 9 millones 
y se cambió el tipo de dato en la migración a `bigInteger` para 
soportar propiedades de alto valor. Esto previene la caída del 
servidor y devuelve un mensaje de error legible al frontend.