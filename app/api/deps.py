from typing import Generator, Dict, Any
from app.db.session import Session, engine
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app import models, schemas
from app.core.config import settings, Settings
from app.core import security
from app.actions.account_admin import AdminAction
from fastapi.security import OAuth2PasswordRequestForm

# login route will give you user JWT token
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/admin/login")


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


def get_current_account(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2),
) -> models.Admin:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

    admin = session.get(models.Admin, token_data.sub)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin Account not found")
    return admin


def login_access_token(
    session: Session,
    form: OAuth2PasswordRequestForm,
    admin_action: AdminAction,
    settings: Settings,
) -> Dict[str, Any]:
    """
    Authenticate the user(admin) and generate an OAuth2-compatible access token.

    Raises:
        HTTPException: If credentials are invalid or the account is inactive.

    Returns:
        Dict[str, Any]: Contains the access token, expiry, token type, and account details.
    """
    account = admin_action.authenticate(
        session, email=form.username.lower(), password=form.password
    )
    if not account:
        raise HTTPException(status_code=400, detail="Incorrect email or password or not an admin")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    session.add(account)
    session.commit()
    return {
        "access_token": security.create_access_token(account.id, settings, access_token_expires),
        "expires": datetime.now(timezone.utc) + access_token_expires,
        "token_type": "bearer",
        "account": account,
    }
