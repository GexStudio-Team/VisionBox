from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

@router.get(
    "/v1/health",
    tags=["System"],
    summary="Health check",
    description="Returns the current status of the VisionBox backend",
)

def health():
    return{
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
