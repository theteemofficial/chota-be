from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated
from sqlmodel import Session
from app.api import deps

from app.actions import recommendation_action as ra, category_action as ca

from app.models import RecommendationRead, RecommendationCreate

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/", response_model=RecommendationRead)
def recommend_business(data: RecommendationCreate, session: CommonSession):
    """
    Endpoint for users to recommend a business
    """
    # ensure categories are provided
    if not data.category_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one category must be provided",
        )
    categories = ca.get_by_ids(session=session, ids=data.category_ids)

    # validate all IDs exist
    if len(categories) != len(set(data.category_ids)):
        existing_ids = {c.id for c in categories}
        missing_ids = set(data.category_ids) - existing_ids

        raise HTTPException(
            status_code=404,
            detail=f"Categories not found: {list(missing_ids)}",
        )

    recommendation = ra.create_recommendation(session=session, data=data)
    return recommendation
