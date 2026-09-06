# VisionBox · research/ai-vision

> Rama de **investigación y prototipado** de la visión por computadora de VisionBox: el módulo que reconocerá objetos en las fotos de la caja para sugerir detecciones que el usuario aprueba, corrige o descarta.

Esta rama parte de la línea base (`main`) y **no toca el código de producto en `develop`**. Aquí se experimenta con modelos y datos para obtener una primera evaluación válida de un detector de objetos; el resultado se integra luego al producto como un servicio separado.

## Objetivo

Que la API de IA reciba una fotografía y devuelva predicciones:

```
imagen ──▶ [detector de objetos] ──▶ [
  { label: "gafas de sol",   confidence: 0.93, bbox: [x1, y1, x2, y2] },
  { label: "audifonos",      confidence: 0.87, bbox: [x1, y1, x2, y2] }
]
```

El backend de producto decide cómo usar estas sugerencias (bandeja de detecciones); la IA **nunca modifica el inventario por su cuenta**.

## Estado

| Actividad | Estado |
| --- | --- |
| Definición del contrato de integración | ✅ Definido (ver `docs/AI_RESEARCH.md`) |
| Recolección y etiquetado de imágenes | 🔬 En evaluación |
| Selección de modelo y preprocesamiento | 🔬 En evaluación |
| Métricas de evaluación (mAP, umbrales) | 🔬 En evaluación |
| Detección simulada para probar el flujo | 🚧 En planificación (pertenece a `develop`) |

## Definición de "listo" para integrar

La integración se considerará lista cuando exista un modelo capaz de generar una **detección pendiente** a partir de una imagen, mostrarla en el panel y registrar una **corrección humana**. No se exige que el modelo sea preciso todavía: la precisión mejora con el uso real.

## Documentación de esta rama

| Documento | Contenido |
| --- | --- |
| [README.md](README.md) | Vista general de la investigación. |
| [docs/AI_RESEARCH.md](docs/AI_RESEARCH.md) | Plan, enfoques, datos, métricas y experimentos. |

## Convenciones

- Trabajar esta rama en pequeños experimentos; cada hallazgo se registra en `docs/AI_RESEARCH.md`.
- Al validar el flujo, compartir el contrato con `develop` y crear un pull request hacia la línea de integración.

---
El contexto completo de producto y del MVP vive en `develop` (documentación en `dev`→`docs/`).