from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List
from sqlmodel import Session
from app.api import deps, rbac

from app.actions import recommendation_action as ra

from app.models import RecommendationRead, AccountRole

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.get("/", response_model=List[RecommendationRead])
def get_recommendations(
    session: CommonSession,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
):
    """
    Endpoint for admin to get all business recommendations
    """
    return ra.get_all(session)


@router.get("/{id}", response_model=RecommendationRead)
def get_recommendation(
    id: int,
    session: CommonSession,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
):
    """
    Endpoint for admin to get a business recommendation by id
    """

    recommendation = ra.get_by_id(session, id)

    if not recommendation:
        raise HTTPException(404, detail="Recommendation not found")

    return recommendation
