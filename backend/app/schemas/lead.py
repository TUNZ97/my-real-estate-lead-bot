"""Lead schemas."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    intent: Optional[str] = None
    property_type: Optional[str] = None
    location_text: Optional[str] = None
    bedrooms: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    timeframe: Optional[str] = None
    assigned_to: Optional[UUID] = None


class LeadResponse(BaseModel):
    id: UUID
    customer_id: UUID
    status: str
    intent: Optional[str] = None
    property_type: Optional[str] = None
    location_text: Optional[str] = None
    bedrooms: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    timeframe: Optional[str] = None
    qualification_level: Optional[str] = None
    qualification_score: Optional[int] = None
    urgency: Optional[str] = None
    assigned_to: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadListResponse(BaseModel):
    items: List[LeadResponse] = Field(default_factory=list)
    total: int = 0
    limit: int = 20
    offset: int = 0
