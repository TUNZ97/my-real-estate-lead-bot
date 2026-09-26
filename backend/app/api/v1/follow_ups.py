"""Follow-up endpoints."""

from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_follow_up():
    """Create a follow-up for a lead."""
    # TODO: implement
    raise NotImplementedError


@router.patch("/{follow_up_id}")
async def update_follow_up(follow_up_id: UUID):
    """Update follow-up status or completion."""
    # TODO: implement
    raise NotImplementedError
