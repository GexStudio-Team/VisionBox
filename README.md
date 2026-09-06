# VisionBox

> Caja de almacenamiento inteligente con visión por computadora para registrar, controlar y gestionar objetos personales de forma automática.

VisionBox combina un **panel web de inventario**, una **API REST** y una futura **inteligencia artificial de detección de objetos** para que sepas qué tienes, dónde está y qué entra o sale de tu caja. Hoy funciona como un inventario manual completo; mañana la IA te sugerirá detecciones que tú apruebas, corriges o descartas.

## Estado del proyecto

```
main (estable) ───────────────────▶ línea publicada / lista para integrar
develop (desarrollo activo) ──────▶ MVP de inventario funcional  ⭐ rama actual
research/ai-vision (investigación) ▶ visión por computadora (en estudio)
```

## Características

| Área | Estado |
| --- | --- |
| Inventario: crear, editar, archivar, buscar y filtrar objetos | ✅ Desarrollado |
| Historial inmutable de movimientos por objeto | ✅ Desarrollado |
| Panel con métricas (totales, activos, archivados, unidades) | ✅ Desarrollado |
| API REST versionada + documentación Swagger | ✅ Desarrollado |
| Arranque automatizado con WSL 2 (PostgreSQL + API) | ✅ Desarrollado |
| Autenticación de administrador | 🚧 Planificado |
| Bandeja de detecciones (aprobación humana de la IA) | 🚧 Planificado |
| Detección simulada para probar el flujo | 🚧 Siguiente paso |
| Reconocimiento real de objetos (visión por computadora) | 🔬 En research/ai-vision |

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Frontend | React 19 · TypeScript · Vite |
| Backend / API | Python · FastAPI · SQLAlchemy 2 · Uvicorn |
| Base de datos | PostgreSQL 18 (bajo WSL 2 / Ubuntu 26.04) |
| Infraestructura | WSL 2 · systemd · scripts PowerShell y VBS |
| Alternativa contenedores | Docker Compose (`compose.yaml`) |

## Arquitectura en una frase

Frontend en **Windows** → `http://localhost:5173` ⇄ API en `http://localhost:8000` ⇄ **FastAPI + PostgreSQL dentro de Ubuntu WSL** (loopback nativo estable). Detalle completo en [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Inicio rápido

### Opción A — Un solo clic (Windows)

El backend y la base de datos arrancan solos con WSL. Para levantar todo:

```powershell
& "...\VisionBots-App\scripts\Start-VisionBots.ps1"
```

### Opción B — Manual

```powershell
# Backend + base de datos (ya instalados como servicios en WSL)
wsl -d Ubuntu -u root -- sh -c "service postgresql start; systemctl start visionbots-backend"

# Frontend
cd frontend
npm install
npm run dev
```

Luego abre:

- Panel web: <http://localhost:5173>
- Documentación interactiva de la API: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/v1/health>

Guía completa: [`docs/LOCAL_DEVELOPMENT.md`](docs/LOCAL_DEVELOPMENT.md).

## Estructura del repositorio

```
VisionBox/
├── backend/                  # API REST (FastAPI + SQLAlchemy)
│   ├── app/
│   │   ├── api/              # Routers: health, system, inventory, dashboard
│   │   ├── core/             # Configuración central (.env)
│   │   ├── models/           # Modelos SQLAlchemy (items, item_events)
│   │   ├── schemas/          # Contratos Pydantic de entrada/salida
│   │   └── main.py           # Punto de entrada de la API
│   ├── .env.example          # Plantilla de variables de entorno
│   └── requirements.txt      # Dependencias Python
├── frontend/                 # Panel web (React + TypeScript + Vite)
│   └── src/                  # Componentes, API client y estilos
├── docs/                     # Toda la documentación del proyecto
├── scripts/                  # Operación: Start-VisionBots.ps1 y keep-alive WSL
├── compose.yaml              # PostgreSQL en Docker (alternativa)
└── README.md
```

## Ramas

| Rama | Propósito |
| --- | --- |
| `main` | Estable. Solo recibe versiones probadas (no se edita directamente). |
| `develop` | Integración del desarrollo en curso (inventario MVP). |
| `research/ai-vision` | Investigación de visión por computadora para la futura IA. |

## Documentación

| Documento | Contenido |
| --- | --- |
| [README.md](README.md) | Vista general, inicio rápido y estructura. |
| [docs/PRODUCT_FOUNDATION.md](docs/PRODUCT_FOUNDATION.md) | Visión del producto y alcance del MVP. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Arquitectura, componentes y decisiones técnicas. |
| [docs/API_REFERENCE.md](docs/API_REFERENCE.md) | Referencia de todos los endpoints con ejemplos. |
| [docs/DATABASE.md](docs/DATABASE.md) | Esquema, credenciales y consultas de la base de datos. |
| [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) | Ejecución local, WSL y solución de problemas. |
| [docs/PROGRESS_REPORT.html](docs/PROGRESS_REPORT.html) | Informe visual del avance y glosario técnico. |

## Roadmap

1. ✅ Contratos API, entidades y base de datos PostgreSQL.
2. ✅ CRUD de inventario y registro de actividad en FastAPI.
3. ✅ Panel web con inventario y detecciones.
4. 🔜 Carga de imágenes y detección simulada para probar el flujo.
5. 🔬 Servicio de IA real de reconocimiento de objetos.