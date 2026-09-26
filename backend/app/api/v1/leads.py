"""Lead endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.lead import LeadListResponse, LeadResponse, LeadUpdate
from app.services.lead_service import LeadService
from app.services.qualification_service import QualificationService

router = APIRouter()


@router.get("", response_model=LeadListResponse)
async def list_leads(
    status_filter: Optional[str] = Query(None, alias="status"),
    qualification: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db_session),
):
    service = LeadService(session)
    return await service.list_leads(
        status=status_filter,
        qualification=qualification,
        limit=limit,
        offset=offset,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    service = LeadService(session)
    lead = await service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return LeadResponse.model_validate(lead)


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    payload: LeadUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    service = LeadService(session)
    lead = await service.update_lead(lead_id, payload)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return LeadResponse.model_validate(lead)


@router.post("/{lead_id}/qualify", response_model=LeadResponse)
async def qualify_lead(
    lead_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    service = LeadService(session)
    lead = await service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

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
    return LeadResponse.model_validate(lead)


@router.post("/{lead_id}/handoff")
async def handoff_lead(
    lead_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    service = LeadService(session)
    lead = await service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    lead.status = "CONTACTED"
    await session.flush()
    return {"status": "escalated", "lead_id": lead_id}
