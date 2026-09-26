"""Lead model — property-sales/rental opportunity.

Status, qualification, and urgency are separate concepts.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("customers.id"), nullable=False, index=True
    )

    status: Mapped[str] = mapped_column(String(50), default="NEW", index=True)

    intent: Mapped[str | None] = mapped_column(String(50), nullable=True)
    property_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    location_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_min: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    budget_max: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True, default="NGN")
    timeframe: Mapped[str | None] = mapped_column(String(50), nullable=True)

    qualification_level: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    qualification_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    urgency: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    qualification_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    assigned_to: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    customer = relationship("Customer", back_populates="leads")
    conversations = relationship("Conversation", back_populates="lead")
    activities = relationship("LeadActivity", back_populates="lead")
    follow_ups = relationship("FollowUp", back_populates="lead")
    notifications = relationship("Notification", back_populates="lead")
