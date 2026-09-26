"""Lead endpoints.

GET /api/leads
GET /api/leads/{lead_id}
PATCH /api/leads/{lead_id}
POST /api/leads/{lead_id}/status
POST /api/leads/{lead_id}/qualify
POST /api/leads/{lead_id}/handoff
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query

from app.schemas.lead import LeadListResponse, LeadResponse, LeadUpdate

router = APIRouter()


@router.get("", response_model=LeadListResponse)
async def list_leads(
    status: Optional[str] = Query(None),
    qualification: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List leads with optional filters."""
    # TODO: implement
    return LeadListResponse(items=[], total=0, limit=limit, offset=offset)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: UUID):
    """Get authoritative lead details."""
    # TODO: implement
    raise NotImplementedError


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: UUID, payload: LeadUpdate):
    """Update permitted lead fields."""
    # TODO: implement
    raise NotImplementedError


@router.post("/{lead_id}/qualify")
async def qualify_lead(lead_id: UUID):
    """Run deterministic qualification and persist result."""
    # TODO: implement via QualificationService
    raise NotImplementedError


@router.post("/{lead_id}/handoff")
async def handoff_lead(lead_id: UUID):
    """Escalate conversation to human agent."""
    # TODO: implement
    raise NotImplementedError
