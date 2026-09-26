"""Internal endpoints for n8n callbacks."""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_db_session
from app.services.lead_service import LeadService
from app.services.qualification_service import QualificationService

router = APIRouter()


def verify_n8n_secret(x_n8n_secret: Optional[str] = Header(None)):
    expected = settings.N8N_WEBHOOK_SECRET
    if expected and expected != "change-me" and x_n8n_secret != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret")


class QualifyRequest(BaseModel):
    lead_id: str


@router.post("/qualify")
async def internal_qualify(
    body: QualifyRequest,
    session: AsyncSession = Depends(get_db_session),
    _: None = Depends(verify_n8n_secret),
):
    service = LeadService(session)
    lead = await service.get_lead(body.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    qualifier = QualificationService()
    result = qualifier.calculate(
        {
            "intent": lead.intent,
            "budget_min": float(lead.budget_min) if lead.budget_min is not None else None,
            "budget_max": float(lead.budget_max) if lead.budget_max is not None else None,
            "timeframe": lead.timeframe,
            "location_text": lead.location_text,
            "property_type": lead.property_type,
            "bedrooms": lead.bedrooms,
        }
    )
    lead.qualification_score = result.score
    lead.qualification_level = result.qualification_level
    lead.urgency = result.urgency
    lead.qualification_version = result.version
    await session.flush()

    return {
        "lead_id": lead.id,
        "score": result.score,
        "qualification": result.qualification_level,
        "urgency": result.urgency,
        "version": result.version,
    }


@router.get("/leads/{lead_id}")
async def internal_get_lead(
    lead_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: None = Depends(verify_n8n_secret),
):
    service = LeadService(session)
    lead = await service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        "id": lead.id,
        "status": lead.status,
        "intent": lead.intent,
        "property_type": lead.property_type,
        "location_text": lead.location_text,
        "bedrooms": lead.bedrooms,
        "budget_min": float(lead.budget_min) if lead.budget_min else None,
        "budget_max": float(lead.budget_max) if lead.budget_max else None,
        "currency": lead.currency,
        "timeframe": lead.timeframe,
        "qualification_level": lead.qualification_level,
        "qualification_score": lead.qualification_score,
        "urgency": lead.urgency,
    }
