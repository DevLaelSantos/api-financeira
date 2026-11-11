from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "projeto": settings.PROJECT_NAME,
        "versao": settings.VERSION
    }