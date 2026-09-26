"""Health endpoints (also available at root /health and /ready)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def api_health():
    return {"status": "ok"}
