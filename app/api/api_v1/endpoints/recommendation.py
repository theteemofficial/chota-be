from fastapi import APIRouter, Depends

from typing import Annotated
from sqlmodel import Session
from app.api import deps

from app.actions import recommendation_action as ra

from app.models import RecommendationRead, RecommendationCreate

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/", response_model=RecommendationRead)
def recommend_business(data: RecommendationCreate, session: CommonSession):
    """
    Endpoint for users to recommend a business
    """
    # validate category here

    recommendation = ra.create_recommendation(session=session, data=data)
    return recommendation
