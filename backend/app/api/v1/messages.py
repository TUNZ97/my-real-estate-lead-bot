"""Message intake endpoints — FR-001."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter()


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit customer message",
)
async def create_message(
    payload: MessageCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Accept a customer message, persist it, extract requirements,
    qualify the lead, generate a grounded response, and return it.

    Idempotent when external_message_id is supplied.
    """
    service = MessageService(session)
    return await service.process_message(payload)
