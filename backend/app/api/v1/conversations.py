"""Conversation endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db_session
from app.models.conversation import Conversation
from app.models.message import Message

router = APIRouter()


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .options(selectinload(Conversation.messages))
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {
        "id": str(conv.id),
        "customer_id": str(conv.customer_id),
        "lead_id": str(conv.lead_id) if conv.lead_id else None,
        "status": conv.status,
        "channel": conv.channel,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
    }


@router.get("/{conversation_id}/messages")
async def list_messages(
    conversation_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return {
        "items": [
            {
                "id": str(m.id),
                "sender_type": m.sender_type,
                "content": m.content,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ]
    }
