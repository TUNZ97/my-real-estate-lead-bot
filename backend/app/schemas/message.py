"""Message request/response schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=10000)
    external_message_id: Optional[str] = None
    channel: str = "web"
    customer_id: Optional[str] = None


class MessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: Optional[str] = None
    lead_id: Optional[str] = None
