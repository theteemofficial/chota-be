from sqlmodel import Field
from typing import TYPE_CHECKING

from .base import ModelBase

if TYPE_CHECKING:
    from .business import Business  # noqa: F401
    from .category import Category  # noqa: F401


class BusinessCategory(ModelBase, table=True):
    business_id: int = Field(foreign_key="business.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)
