from pydantic.networks import EmailStr
from sqlmodel import Field
from typing import Optional

from .cho_enum import BaseEnum
from .base import ModelBase


class AccountRole(BaseEnum):
    admin = "admin"


class AdminBase(ModelBase):
    email: EmailStr = Field(unique=True, index=True)
    is_superuser: bool = True
    role: AccountRole = AccountRole.admin


class Admin(AdminBase, table=True):
    hashed_password: Optional[str]
