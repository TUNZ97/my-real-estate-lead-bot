"""Message intake endpoints — FR-001.

POST /api/messages — submit a customer message (idempotent via external_message_id).
"""

from fastapi import APIRouter, status

from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter()


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit customer message",
)
async def create_message(payload: MessageCreate):
    """
    Accept a customer message, persist it, and trigger downstream processing.

    Idempotency: if external_message_id is supplied and already exists,
    return the existing result without creating duplicates.
    """
    # TODO: implement via MessageService
    return MessageResponse(
        conversation_id=payload.conversation_id or "conv_placeholder",
        message_id="msg_placeholder",
        response="Thanks for your enquiry. We are processing it.",
        lead_id=None,
    )
