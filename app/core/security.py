from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import bcrypt
from app.core.config import Settings
from typing import Union, Any, Optional
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Returns:
        str: The securely hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain_password matches its hashed one.
    Returns: True if it does, else Return Flase
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(
    subject: Union[str, Any],
    settings: Settings,
    expiry_minutes: Optional[Union[timedelta, int]] = 11520,
) -> str:
    """
    Generate a signed JSON Web Token (JWT) for authentication.
    Returns: The JWT as a string
    """

    to_encode = {"sub": str(subject)}
    if expiry_minutes:
        if isinstance(expiry_minutes, int):
            expiry_minutes = timedelta(minutes=expiry_minutes)
        expire = datetime.now(timezone.utc) + expiry_minutes
        to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
