from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_session
from app.crud.interaction import (
    create_interaction as crud_create,
    get_interactions as crud_list,
    get_interaction_by_id as crud_get,
    update_interaction as crud_update,
)
from app.crud.hcp import get_hcp_by_id
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionResponse

router = APIRouter()


@router.post("/interactions", summary="Create interaction", status_code=201, response_model=InteractionResponse)
async def create_interaction_endpoint(
    payload: InteractionCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new interaction record."""
    # Verify HCP exists
    hcp = await get_hcp_by_id(session, payload.hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    data = payload.model_dump()

    # Auto-populate location from HCP institution
    if not data.get("location") and hcp.institution:
        data["location"] = hcp.institution

    # Extract samples separately
    samples = data.pop("samples", None) or []
    data["samples"] = [{"product_name": s["product_name"], "quantity": s["quantity"]} for s in samples]

    interaction = await crud_create(session, data)
    return interaction


@router.get("/interactions", summary="List interactions", response_model=list[InteractionResponse])
async def list_interactions_endpoint(
    hcp_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """Get paginated list of interactions."""
    interactions = await crud_list(session, hcp_id=hcp_id, limit=limit, offset=offset)
    return interactions


@router.get("/interactions/{interaction_id}", summary="Get interaction", response_model=InteractionResponse)
async def get_interaction_endpoint(
    interaction_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a single interaction."""
    interaction = await crud_get(session, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.put("/interactions/{interaction_id}", summary="Update interaction", response_model=InteractionResponse)
async def update_interaction_endpoint(
    interaction_id: int,
    payload: InteractionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Partial update an interaction."""
    data = payload.model_dump(exclude_unset=True)
    interaction = await crud_update(session, interaction_id, data)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction
