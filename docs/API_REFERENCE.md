# Referencia de la API de VisionBox

- **Base URL local:** `http://localhost:8000/api/v1`
- **Documentación interactiva (Swagger UI):** <http://localhost:8000/docs>
- **Formato:** JSON
- **Prefijo y versión:** configurables en `backend/.env` (`API_PREFIX`, `API_VERSION`).

## Estados de un objeto

`status`: `active` (activo) · `archived` (archivado).

## Errores

| Código | Significado |
| --- | --- |
| 404 | Recurso no encontrado (detalle `"Item not found"`). |
| 422 | Validación fallida (cuerpo inválido, parámetros fuera de rango). |
| 500 | Error interno. |

---

## System

### `GET /health`

Estado del backend.

```http
GET /api/v1/health
```

```json
{ "status": "online", "service": "VisionBots API", "version": "0.1.0" }
```

### `GET /system`

Información del sistema y versión de la API.

```http
GET /api/v1/system
```

```json
{
  "status": "running",
  "project": "VisionBots API",
  "version": "0.1.0",
  "api": { "prefix": "/api", "version": "v1" }
}
```

---

## Dashboard

### `GET /dashboard`

Resumen del inventario.

```http
GET /api/v1/dashboard
```

```json
{
  "total_items": 2,
  "active_items": 1,
  "archived_items": 1,
  "total_units": 3,
  "recent_events": [
    { "id": 4, "item_id": 1, "action": "archived", "detail": "Item archived", "created_at": "2026-09-05T10:00:00Z" }
  ]
}
```

---

## Inventory

### `GET /inventory`

Lista el inventario con filtros y paginación.

| Query | Tipo | Descripción |
| --- | --- | --- |
| `search` | string | Filtra por nombre (insensible a mayúsculas). |
| `category` | string | Filtra por categoría exacta. |
| `status` | `active` \| `archived` | Filtra por estado. |
| `limit` | int (1–100, def. 50) | Máximo de filas. |
| `offset` | int (def. 0) | Desplazamiento. |

```http
GET /api/v1/inventory?search=audif&limit=20
```

```json
[
  {
    "id": 1,
    "name": "Audifonos Sony",
    "category": "Electronica",
    "description": null,
    "quantity": 2,
    "location": "Caja principal",
    "image_url": null,
    "status": "active",
    "created_at": "2026-09-05T09:00:00Z",
    "updated_at": "2026-09-05T09:10:00Z"
  }
]
```

### `POST /inventory`

Crea un objeto. Respuesta `201`.

```http
POST /api/v1/inventory
Content-Type: application/json
```

```json
{
  "name": "Audifonos Sony",
  "category": "Electronica",
  "quantity": 1,
  "location": "Caja principal",
  "description": "Inalambricos, color negro"
}
```

### `GET /inventory/{item_id}`

Devuelve un objeto por su id.

### `PATCH /inventory/{item_id}`

Actualiza solo los campos enviados. Soporta `status`.

```http
PATCH /api/v1/inventory/1
Content-Type: application/json
```

```json
{ "quantity": 3, "location": "Cajon de arriba" }
```

### `POST /inventory/{item_id}/archive`

Archiva un objeto (pasa su estado a `archived`).

### `GET /inventory/{item_id}/events`

Historial inmutable del objeto, del más reciente al más antiguo.

```http
GET /api/v1/inventory/1/events
```

```json
[
  { "id": 3, "item_id": 1, "action": "updated", "detail": "Item fields updated", "created_at": "2026-09-05T09:10:00Z" },
  { "id": 1, "item_id": 1, "action": "created", "detail": "Item created manually", "created_at": "2026-09-05T09:00:00Z" }
]
```

---

## Contrato de un objeto (Item)

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | int | Identificador único. |
| `name` | string (1–160) | Nombre del objeto. Obligatorio. |
| `category` | string (≤80) \| null | Categoría. |
| `description` | string \| null | Descripción libre. |
| `quantity` | int ≥ 0 | Cantidad de unidades (def. 1). |
| `location` | string (≤120) \| null | Ubicación física (caja, cajón…). |
| `image_url` | string (≤500) \| null | Referencia a foto. Se usa al añadir carga de imágenes. |
| `status` | `active` \| `archived` | Estado actual. |
| `created_at` / `updated_at` | datetime | Marca de tiempo (zona con hora). |