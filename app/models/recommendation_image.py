from .base import ModelBase, SchemaBase
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .recommendation import Recommendation


class RecommendationImageBase(ModelBase):
    recommendation_id: int = Field(foreign_key="recommendation.id")
    image: str


class RecommendationImage(RecommendationImageBase, table=True):
    recommendation: "Recommendation" = Relationship(back_populates="images")


class RecommendationImageCreate(SchemaBase):
    image: str


class RecommendationImageUpdate(SchemaBase):
    business_id: Optional[int] = None
    image: Optional[str] = None


class RecommendationImageRead(RecommendationImageBase):
    id: int
