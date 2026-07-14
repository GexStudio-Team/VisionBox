from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    tittle=settings.PROJECT_NAME,
    version=settings.VERSION
)


@app.get("/")
def root():
    return{
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Backend Running"
    }