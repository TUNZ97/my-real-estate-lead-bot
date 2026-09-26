"""Lead domain service."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.schemas.lead import LeadListResponse, LeadResponse, LeadUpdate


class LeadService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_leads(
        self,
        status: Optional[str] = None,
        qualification: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> LeadListResponse:
        query = select(Lead).order_by(Lead.created_at.desc())
        count_query = select(func.count()).select_from(Lead)

        if status:
            query = query.where(Lead.status == status)
            count_query = count_query.where(Lead.status == status)
        if qualification:
            query = query.where(Lead.qualification_level == qualification)
            count_query = count_query.where(Lead.qualification_level == qualification)

        total = (await self.session.execute(count_query)).scalar() or 0
        result = await self.session.execute(query.limit(limit).offset(offset))
        leads = result.scalars().all()

        return LeadListResponse(
            items=[LeadResponse.model_validate(l) for l in leads],
            total=total,
            limit=limit,
            offset=offset,
        )

    async def get_lead(self, lead_id: uuid.UUID) -> Optional[Lead]:
        result = await self.session.execute(select(Lead).where(Lead.id == lead_id))
        return result.scalar_one_or_none()

    async def update_lead(self, lead_id: uuid.UUID, payload: LeadUpdate) -> Optional[Lead]:
        lead = await self.get_lead(lead_id)
        if not lead:
            return None
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(lead, key, value)
        await self.session.flush()
        return lead
