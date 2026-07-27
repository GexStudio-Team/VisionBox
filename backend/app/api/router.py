from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.system import router as system_router
from app.api.inventory import router as inventory_router
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}"
)

api_router.include_router(
    system_router,
    prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}"
)

api_router.include_router(
    inventory_router,
    prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}"
)