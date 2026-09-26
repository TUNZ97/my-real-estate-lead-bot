"""Conversation endpoints."""

from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: UUID):
    """Get conversation details."""
    # TODO: implement
    raise NotImplementedError


@router.get("/{conversation_id}/messages")
async def list_messages(conversation_id: UUID):
    """List messages for a conversation (chronological)."""
    # TODO: implement
    raise NotImplementedError
