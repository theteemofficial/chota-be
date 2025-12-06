from sqlmodel import Field
from typing import TYPE_CHECKING

from .base import SchemaBase

if TYPE_CHECKING:
    from .recommendation import Recommendation  # noqa: F401
    from .category import Category  # noqa: F401


class RecommendationCategory(SchemaBase, table=True):
    recommendation_id: int = Field(foreign_key="recommendation.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)
