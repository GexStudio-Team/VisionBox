from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import api_router

from app.db import Base, engine
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


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
    """,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(api_router)
