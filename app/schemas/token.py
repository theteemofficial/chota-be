from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import Admin


class Token(BaseModel):
    access_token: str
    expires: datetime
    token_type: str
    account: Admin


class TokenPayload(BaseModel):
    sub: Optional[int] = None
