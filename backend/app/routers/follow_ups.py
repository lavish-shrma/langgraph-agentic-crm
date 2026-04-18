from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_session
from app.crud.follow_up import (
    create_follow_up as crud_create,
    get_follow_ups as crud_list,
    update_follow_up as crud_update,
)
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate, FollowUpResponse

router = APIRouter()


@router.post("/follow-ups", summary="Create follow-up", status_code=201, response_model=FollowUpResponse)
async def create_follow_up_endpoint(
    payload: FollowUpCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new follow-up."""
    data = payload.model_dump()
    follow_up = await crud_create(session, data)
    return follow_up


@router.get("/follow-ups", summary="List follow-ups", response_model=list[FollowUpResponse])
async def list_follow_ups_endpoint(
    hcp_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    """Get filtered list of follow-ups."""
    follow_ups = await crud_list(session, hcp_id=hcp_id, status=status)
    return follow_ups


@router.put("/follow-ups/{follow_up_id}", summary="Update follow-up", response_model=FollowUpResponse)
async def update_follow_up_endpoint(
    follow_up_id: int,
    payload: FollowUpUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update a follow-up."""
    data = payload.model_dump(exclude_unset=True)
    follow_up = await crud_update(session, follow_up_id, data)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return follow_up
