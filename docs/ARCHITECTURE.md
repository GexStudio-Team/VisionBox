# Arquitectura de VisionBox

Este documento describe cómo está compuesto el sistema, cómo fluyen los datos y por qué se tomaron las decisiones técnicas actuales.

## Visión general

```
┌─────────────────────────────────────────────────────────────────┐
│  WINDOWS                                                         │
│                                                                  │
│   Navegador (React + Vite)          ┌────────────────────┐       │
│   http://localhost:5173 ──────────▶ │  API en localhost  │       │
│        │                             │  :8000             │       │
│        │  Fetch / JSON               └──────────┬─────────┘       │
│        └────────────────────────────────────────┘                │
└───────────────────────────────────────────────────────────────────┘
                                  │  HTTP 0.0.0.0:8000
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  WSL 2 · Ubuntu 26.04                                           │
│                                                                  │
│   FastAPI (uvicorn, servicio) ──▶ loopback nativo 127.0.0.1     │
│        │   /api/v1/*                                            │
│        ▼                                                        │
│   PostgreSQL 18  (base: visionbots · puerto 5432)               │
│   tables: items, item_events                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes

### Frontend (`frontend/`)

- **React 19 + TypeScript + Vite**. Se ejecuta en Windows y compila con `npm run build`.
- `src/api.ts` centraliza todas las llamadas al backend. La URL base por defecto es
  `http://localhost:8000/api/v1` y puede sobrescribirse con `VITE_API_URL` (ver `frontend/.env.example`).
- `src/App.tsx` implementa el panel: métricas, creación de objetos, búsqueda y archivado.

### Backend (`backend/`)

Aplicación **FastAPI** organizada en capas:

| Carpeta | Responsabilidad |
| --- | --- |
| `app/api/` | Routers HTTP. Cada archivo agrupa endpoints por dominio (health, system, inventory, dashboard). |
| `app/core/config.py` | Configuración central leída del `.env` (proyecto, versión, prefijo, base de datos, CORS). |
| `app/models/` | Modelos SQLAlchemy que definen las tablas. |
| `app/schemas/` | Contratos Pydantic: validación de entrada y serialización de salida. |
| `app/db.py` | Motor de base de datos, pool y sesiones (`get_db`). |
| `app/main.py` | Crea la app, configura CORS, crea tablas al arrancar (`lifespan`) y monta los routers. |

### Base de datos

- **PostgreSQL 18** corriendo dentro de Ubuntu WSL como servicio systemd.
- Motor de acceso: **SQLAlchemy 2 + psycopg 3**.
- Configuración de conexión en `backend/.env` (`DATABASE_URL`).

## Flujo de una petición

1. El navegador llama, por ejemplo, `POST /api/v1/inventory` con un `JSON`.
2. FastAPI valida el cuerpo contra el esquema `ItemCreate` (Pydantic).
3. El router `inventory.py` usa la sesión `get_db` y crea el objeto `Item`.
4. Se registra un `ItemEvent` (action `created`) en el historial.
5. Se confirma con `commit` y se devuelve `ItemResponse` serializado.
6. El frontend refresca lista y métricas.

## Decisiones técnicas (registro breve)

| Decisión | Por qué |
| --- | --- |
| Backend + PostgreSQL juntos en WSL | Las conexiones TCP persistentes Windows→WSL son inestables aquí; en loopback nativo dentro de Linux son 100% estables. |
| FastAPI (y no otro framework) | El backend ya usa Python y el equipo de IA puede compartir validaciones y contratos. |
| PostgreSQL desde el inicio | Robustez para inventario, auditoría y relaciones; evita migrar desde SQLite después. Los archivos (fotos/videos) no se guardan como blobs: se almacenan referencias. |
| IA como servicio separado | El panel y el inventario siguen disponibles aunque el modelo tarde o falle. |
| Servicios systemd + keep-alive | PostgreSQL y la API arrancan solos al encender la VM de WSL; un script de Inicio de Windows mantiene viva la VM. |
| Pool con pre_ping y reciclado | Conexiones cortadas por la red se detectan y se recuperan sin colgar el servidor. |

## Límites entre servicios

El backend de producto es **dueño del inventario y los usuarios**. La futura IA solo recibe una imagen o referencia de archivo y devuelve predicciones. Una predicción **no modifica el inventario** hasta que el backend aplique una regla o un usuario humano la confirme (bandeja de detecciones).

## Alternativa con contenedores

`compose.yaml` define PostgreSQL 17 en Docker con las mismas credenciales. Está documentada como alternativa futura; hoy el sistema no depende de Docker.