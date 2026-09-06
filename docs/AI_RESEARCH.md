# Investigación de IA · Visión para VisionBox

Plan de investigación para el módulo que reconoce objetos en imágenes de la caja
de almacenamiento y produce **sugerencias de detección** para el producto.

## 1. Objetivo del módulo

Dado `{"image_url": "s3://.../foto.jpg"}` el servicio responde:

```json
{
  "detections": [
    { "label": "gafas-de-sol", "confidence": 0.93, "bbox": [12, 34, 210, 180] },
    { "label": "audifonos",    "confidence": 0.87, "bbox": [300, 60, 480, 260] }
  ]
}
```

- **Entrada:** una imagen o referencia a un archivo.
- **Salida:** etiqueta, nivel de confianza y caja delimitadora (bbox).
- **Regla:** una predicción no modifica el inventario. La aplica el backend de
  producto o un usuario humano (bandeja de detecciones).

## 2. Alcance y límites

Qué sí:

- Detectar objetos cotidianos en una caja/cajón con iluminación controlada.
- Probar rápido: carga de imágenes + detección simulada antes de entrenar.

Qué no (por ahora):

- Inventario, usuarios o lógica de negocio (eso vive en `develop`).
- Mapas completos de la caja o localización 3D.
- Optimización para dispositivos embebidos.

## 3. Enfoques a evaluar

| Enfoque | Para qué | Herramientas candidatas |
| --- | --- | --- |
| Detección pre-entrenada | Arrancar sin datos | Ultralytics YOLOv8/, OpenCV |
| Fine-tuning del detector | Ajustar a objetos propios | Ultralytics, PyTorch |
| Preprocesamiento | Iluminación, recortes, máscara de fondo | OpenCV, Pillow |
| Incremento por uso real | Etiquetas desde correcciones humanas | Pipeline de `develop` |

Decisiones pendientes de experimentar:

1. ¿Detección general o clasificación + localización?
2. ¿Qué versión de modelo cabe para probar en 1-2 inferencias por segundo?
3. ¿Umbral de confianza por clase o uno global?

## 4. Datos

- Las fotos de prueba vienen de la cámara real (celular o USB) en distintas
  condiciones de luz.
- Cada imagen se etiqueta con clases y bboxes. Una detección corregida por el
  usuario en el producto **se guarda como etiqueta de entrenamiento**: el uso del
  día a día genera el dataset.
- Las imágenes **no** van a Git. Se guardan en almacenamiento local (desarrollo)
  o S3/MinIO (producción); en el repo solo van referencias.

## 5. Métricas y criterio de aceptación

- **mAP@0.5** como métrica principal; revisar precisión por clase.
- La integración se considera lista cuando:
  - el flujo genera una detección pendiente desde una imagen;
  - el panel la muestra;
  - y se puede registrar una corrección humana.
- No se exige precisión alta al principio: la exactitud mejora con el uso real.

## 6. Entorno de investigación

Python. Sin instalarlo en el proyecto de producto; recomendado un paquete
experimental (entorno virtual propio de esta rama). Se evaluará dockerizar el
servicio al integrarlo.

## 7. Bitácora de experimentos

| # | Fecha | Hipótesis | Script | Resultado | Decisión |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — |

## 8. Entregables de la rama

1. Este documento actualizado según avanza la investigación.
2. Un contrato funcional que `develop` pueda consumir.
3. (Cuando aplique) un servicio mínimo de inferencia con su README propio.