"""AI / rule-based extraction schema — aligned with AI_SPECIFICATION.md."""

from typing import List, Optional

from pydantic import BaseModel, Field


class CustomerExtract(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ExtractionResult(BaseModel):
    intent: Optional[str] = Field(
        None,
        description="BUY | RENT | SELL | PROPERTY_ENQUIRY | GENERAL_ENQUIRY | UNKNOWN",
    )
    property_type: Optional[str] = Field(
        None,
        description="APARTMENT | HOUSE | DUPLEX | LAND | OFFICE | COMMERCIAL | OTHER | UNKNOWN",
    )
    bedrooms: Optional[int] = None
    location: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    currency: Optional[str] = "NGN"
    timeframe: Optional[str] = Field(
        None,
        description="IMMEDIATE | WITHIN_1_MONTH | WITHIN_3_MONTHS | OVER_3_MONTHS | RESEARCHING | UNKNOWN",
    )
    customer: Optional[CustomerExtract] = None
    missing_information: List[str] = Field(default_factory=list)
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    requires_human: bool = False
    handoff_reason: Optional[str] = None
    suggested_next_question: Optional[str] = None
    response: Optional[str] = None
