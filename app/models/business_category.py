from sqlmodel import Field
from typing import TYPE_CHECKING

from .base import ModelBase

if TYPE_CHECKING:
    pass


class BusinessCategory(ModelBase, table=True):
    business_id: int = Field(foreign_key="business.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)
