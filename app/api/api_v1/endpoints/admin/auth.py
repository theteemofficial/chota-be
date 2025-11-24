from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any
from sqlmodel import Session
from app.api import deps
from app.schemas import Token
from app.actions import admin_action as aa
from app.core.config import settings

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/login", response_model=Token)
def get_login_access_token(
    session: CommonSession,
    form: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return deps.login_access_token(session, form=form, admin_action=aa, settings=settings)
