from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_session
from app.crud.hcp import search_hcps, get_hcp_by_id
from app.crud.interaction import get_interactions
from app.schemas.hcp import HCPResponse, HCPWithInteractions
from app.schemas.interaction import InteractionResponse

router = APIRouter()


@router.get("/hcps", summary="Search HCPs", response_model=list[HCPResponse])
async def search_hcps_endpoint(
    search: str = Query("", description="Search query for HCP name"),
    session: AsyncSession = Depends(get_session),
):
    """Search healthcare professionals by name."""
    hcps = await search_hcps(session, search)
    return hcps


@router.get("/hcps/{hcp_id}", summary="Get HCP by ID")
async def get_hcp_endpoint(
    hcp_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a single HCP with last 5 interactions."""
    hcp = await get_hcp_by_id(session, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    interactions = await get_interactions(session, hcp_id=hcp_id, limit=5)
    hcp_data = HCPResponse.model_validate(hcp).model_dump()
    hcp_data["interactions"] = [
        InteractionResponse.model_validate(i).model_dump() for i in interactions
    ]
    return hcp_data
