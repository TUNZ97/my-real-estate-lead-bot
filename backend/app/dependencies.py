"""Shared FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

# Placeholder for auth dependencies
# async def get_current_user(...):
#     ...

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
