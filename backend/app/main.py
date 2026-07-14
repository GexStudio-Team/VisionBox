from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    VisionBox API

    Backend oficial del sistema VisionBox.
    Funciones Principales:

    - Gestion de inventario
    - Comunicacion con hardware
    - Porcesamiento de IA
    - Administacion del sistema

    """
)

@app.get(
    "/",
    tags=["System"],
    summary="Root endpoint",
    description="Returns the welcome message of the VisionBox API."
)
def root():
    return {
        "message": "Welcome to VisionBox API"
    }


@app.get( "/health",
    tags=["System"],
    summary="Health Check",
    description="Returns the current status of the VisionBox backend",
)

def health():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }