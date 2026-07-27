from fastapi import APIRouter

from app.schemas.system import SystemResponse
from app.core.config import settings

router = APIRouter()

@router.get(
    "/system",
    response_model=SystemResponse,
    tags=["System"],
    summary="System information",
    description="Returns basic information about the VisionBox backend system."
)

def system_info():
    return {
        "status": "running",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api":{
            "prefix": settings.API_PREFIX,
            "version": settings.API_VERSION
        }
    }