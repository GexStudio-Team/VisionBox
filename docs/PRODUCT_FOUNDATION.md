# VisionBots: base de producto

## Objetivo de la primera versión

Crear una aplicación web desde la que una persona pueda registrar objetos,
consultar su inventario y corregir las detecciones que lleguen de la futura
inteligencia artificial. La aplicación debe ser útil incluso antes de que el
modelo reconozca objetos de forma automática.

## Decisiones propuestas

| Área | Propuesta | Motivo |
| --- | --- | --- |
| Web | React, TypeScript y Vite | Interfaz rápida de desarrollar, sencilla de mantener y adecuada para un panel web. |
| API | FastAPI | El backend actual ya usa Python y puede compartir contratos y validaciones con el proyecto de IA. |
| Datos | PostgreSQL | Permite empezar localmente con Docker y crecer sin migrar desde SQLite; es robusto para inventario, auditoría y relaciones. |
| Archivos | almacenamiento local en desarrollo y S3/MinIO después | Las fotos y videos no deben guardarse como blobs en la base de datos. |
| IA | servicio separado | El panel y el inventario siguen disponibles aunque el modelo tarde o falle. |

Para pruebas muy rápidas se puede usar SQLite de forma temporal, pero la base
de datos de desarrollo compartida debe ser PostgreSQL desde el inicio.

## MVP funcional

1. Autenticación de un administrador.
2. Inventario: crear, editar, archivar, buscar y filtrar objetos.
3. Ubicaciones: caja, compartimento y estado del objeto.
4. Registro de actividad: alta manual, entrada, salida y corrección humana.
5. Bandeja de detecciones: foto, etiqueta sugerida, confianza y decisión de
   aprobar, corregir o descartar.
6. Panel inicial con totales, últimas actividades y detecciones pendientes.

## Modelo de datos inicial

- `users`: administradores y futuros usuarios.
- `boxes` y `compartments`: ubicación física de cada objeto.
- `items`: catálogo e inventario actual.
- `item_events`: historial inmutable de cambios.
- `media_assets`: fotografía o video asociado a un evento.
- `detections`: resultado de la IA, confianza, versión del modelo y revisión
  humana.

La corrección humana de una detección se guarda como etiqueta de entrenamiento.
Así el uso cotidiano de VisionBots genera los datos con los que se mejora el
modelo.

## Límites entre servicios

El backend de producto es el dueño del inventario y de los usuarios. La IA solo
recibe una imagen o referencia de archivo y responde con predicciones. Una
predicción no modifica el inventario hasta que el backend aplique una regla o
un usuario la confirme.

## Orden de implementación

1. Definir contratos API, entidades y migraciones PostgreSQL.
2. Construir CRUD de inventario y el registro de actividad en FastAPI.
3. Crear el panel web y las pantallas de inventario/detecciones.
4. Añadir carga de imágenes y una detección simulada para probar el flujo.
5. Conectar el servicio de IA real cuando tenga una primera evaluación válida.

## Criterio de “listo” para la integración de IA

La interfaz de integración estará lista cuando pueda crear una detección
pendiente a partir de una imagen, mostrarla en el panel y registrar una
corrección humana. No depende de que el modelo sea preciso todavía.
