from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""

    Backend oficial del sistema VisionBox.

Funciones principales:

- Gestión de inventario
- Procesamiento mediante IA
- Comunicación con hardware
- Administración del sistema
"""
)

@app.get(
    "/",
    tags=["System"],
    summary="Root endpoint",
    description="Returns the welcome message of the VisionBox API"
)

def root():
    return {
        "message": "Welcome to the VisionBox API",
    }

app.include_router(health_router)