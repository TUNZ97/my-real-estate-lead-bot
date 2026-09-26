"""Message intake service — core vertical slice (MySQL)."""

from __future__ import annotations

import logging
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.n8n import N8NClient
from app.models.activity import LeadActivity
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.lead import Lead
from app.models.message import Message
from app.schemas.extraction import ExtractionResult
from app.schemas.message import MessageCreate, MessageResponse
from app.services.extraction_service import ExtractionService
from app.services.qualification_service import QualificationService

logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.extractor = ExtractionService()
        self.qualifier = QualificationService()
        self.n8n = N8NClient()

    async def process_message(self, payload: MessageCreate) -> MessageResponse:
        if payload.external_message_id:
            existing = await self._find_by_external_id(payload.external_message_id)
            if existing:
                bot = await self._latest_bot_message(existing.conversation_id)
                lead_id = None
                conv_result = await self.session.execute(
                    select(Conversation).where(Conversation.id == existing.conversation_id)
                )
                conv = conv_result.scalar_one_or_none()
                if conv and conv.lead_id:
                    lead_id = conv.lead_id
                return MessageResponse(
                    conversation_id=existing.conversation_id,
                    message_id=existing.id,
                    response=bot.content if bot else None,
                    lead_id=lead_id,
                )

        conversation, lead, customer = await self._resolve_context(payload)

        customer_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            sender_type="CUSTOMER",
            content=payload.message,
            external_message_id=payload.external_message_id,
        )
        self.session.add(customer_msg)
        await self.session.flush()

        extraction: ExtractionResult = self.extractor.extract(payload.message)
        self._apply_extraction(lead, extraction)

        qual = self.qualifier.calculate(
            {
                "intent": lead.intent,
                "budget_min": float(lead.budget_min) if lead.budget_min is not None else None,
                "budget_max": float(lead.budget_max) if lead.budget_max is not None else None,
                "timeframe": lead.timeframe,
                "location_text": lead.location_text,
                "property_type": lead.property_type,
                "bedrooms": lead.bedrooms,
                "email": customer.email,
                "phone": customer.phone,
            }
        )
        lead.qualification_score = qual.score
        lead.qualification_level = qual.qualification_level
        lead.urgency = qual.urgency
        lead.qualification_version = qual.version

        if extraction.requires_human:
            conversation.status = "ESCALATED"
            lead.status = "CONTACTED"
        elif lead.status == "NEW":
            lead.status = "CONTACTED"

        self.session.add(
            LeadActivity(
                id=str(uuid.uuid4()),
                lead_id=lead.id,
                actor_type="SYSTEM",
                activity_type="MESSAGE_PROCESSED",
                description="Customer message processed and lead updated",
                payload={
                    "message_id": customer_msg.id,
                    "qualification_score": qual.score,
                    "qualification_level": qual.qualification_level,
                    "missing": extraction.missing_information,
                },
            )
        )

        bot_text = (
            extraction.response
            or "Thank you for your message. A sales agent will follow up shortly."
        )
        bot_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            sender_type="BOT",
            content=bot_text,
        )
        self.session.add(bot_msg)
        await self.session.flush()

        try:
            await self.n8n.trigger_workflow(
                "webhook/lead-intake",
                {
                    "event_id": str(uuid.uuid4()),
                    "correlation_id": customer_msg.id,
                    "lead_id": lead.id,
                    "conversation_id": conversation.id,
                    "message_id": customer_msg.id,
                    "message": payload.message,
                    "channel": payload.channel or "web",
                    "extraction": extraction.model_dump(),
                    "qualification": {
                        "score": qual.score,
                        "level": qual.qualification_level,
                        "urgency": qual.urgency,
                        "version": qual.version,
                    },
                    "source": "fastapi",
                    "schema_version": "1.0",
                },
            )
        except Exception as exc:
            logger.warning("n8n webhook failed (non-blocking): %s", exc)

        return MessageResponse(
            conversation_id=conversation.id,
            message_id=customer_msg.id,
            response=bot_text,
            lead_id=lead.id,
        )

    async def _find_by_external_id(self, external_id: str) -> Optional[Message]:
        result = await self.session.execute(
            select(Message).where(Message.external_message_id == external_id)
        )
        return result.scalar_one_or_none()

    async def _latest_bot_message(self, conversation_id: str) -> Optional[Message]:
        result = await self.session.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.sender_type == "BOT",
            )
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _resolve_context(
        self, payload: MessageCreate
    ) -> tuple[Conversation, Lead, Customer]:
        conversation: Optional[Conversation] = None

        if payload.conversation_id:
            result = await self.session.execute(
                select(Conversation).where(Conversation.id == payload.conversation_id)
            )
            conversation = result.scalar_one_or_none()

        if conversation:
            lead = None
            if conversation.lead_id:
                result = await self.session.execute(
                    select(Lead).where(Lead.id == conversation.lead_id)
                )
                lead = result.scalar_one_or_none()
            customer_result = await self.session.execute(
                select(Customer).where(Customer.id == conversation.customer_id)
            )
            customer = customer_result.scalar_one()
            if not lead:
                lead = Lead(
                    id=str(uuid.uuid4()),
                    customer_id=customer.id,
                    status="NEW",
                )
                self.session.add(lead)
                await self.session.flush()
                conversation.lead_id = lead.id
            return conversation, lead, customer

        customer = Customer(id=str(uuid.uuid4()))
        if payload.customer_id:
            result = await self.session.execute(
                select(Customer).where(Customer.id == payload.customer_id)
            )
            existing = result.scalar_one_or_none()
            if existing:
                customer = existing
            else:
                self.session.add(customer)
        else:
            self.session.add(customer)

        await self.session.flush()

        lead = Lead(id=str(uuid.uuid4()), customer_id=customer.id, status="NEW")
        self.session.add(lead)
        await self.session.flush()

        conversation = Conversation(
            id=str(uuid.uuid4()),
            customer_id=customer.id,
            lead_id=lead.id,
            status="ACTIVE",
            channel=payload.channel or "web",
        )
        self.session.add(conversation)
        await self.session.flush()

        return conversation, lead, customer

    @staticmethod
    def _apply_extraction(lead: Lead, extraction: ExtractionResult) -> None:
        if extraction.intent:
            lead.intent = extraction.intent
        if extraction.property_type:
            lead.property_type = extraction.property_type
        if extraction.bedrooms is not None:
            lead.bedrooms = extraction.bedrooms
        if extraction.location:
            lead.location_text = extraction.location
        if extraction.budget_min is not None:
            lead.budget_min = Decimal(str(extraction.budget_min))
        if extraction.budget_max is not None:
            lead.budget_max = Decimal(str(extraction.budget_max))
        if extraction.currency:
            lead.currency = extraction.currency
        if extraction.timeframe:
            lead.timeframe = extraction.timeframe
