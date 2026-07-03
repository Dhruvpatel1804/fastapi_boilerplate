import logging

from app.core.config import settings
from app.db.session import check_db_connection
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=None)
async def health_check():
    """Readiness check — verifies database connectivity."""
    try:
        await check_db_connection()
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": "connected",
        }
    except Exception:
        logger.exception("Database health check failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "environment": settings.ENVIRONMENT,
                "database": "disconnected",
            },
        )
