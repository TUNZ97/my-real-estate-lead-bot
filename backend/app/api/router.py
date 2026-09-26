"""Top-level API router."""

from fastapi import APIRouter

from app.api.v1 import conversations, follow_ups, health, internal, leads, messages

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(follow_ups.router, prefix="/follow-ups", tags=["follow-ups"])
api_router.include_router(internal.router, prefix="/internal", tags=["internal-n8n"])
