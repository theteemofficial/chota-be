# Models for category and sub-category. Self-referencing table
from sqlmodel import Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from .business_category import BusinessCategory
from .recommendation_category import RecommendationCategory

from .base import ModelBase, SchemaBase

if TYPE_CHECKING:
    from .business import Business
    from .recommendation import Recommendation


class CategoryBase(ModelBase):
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Category(CategoryBase, table=True):
    # parent category
    parent: Optional["Category"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Category.id"}
    )

    # sub_category
    children: List["Category"] = Relationship(back_populates="parent")

    businesses: List["Business"] = Relationship(
        back_populates="categories", link_model=BusinessCategory
    )
    recommendations: List["Recommendation"] = Relationship(
        back_populates="categories", link_model=RecommendationCategory
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SchemaBase):
    name: Optional[str] = None
    category_id: Optional[int] = None


class CategoryRead(CategoryBase):
    id: int
