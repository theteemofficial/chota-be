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
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id", nullable=True)


class Category(CategoryBase, table=True):
    # parent category
    parent: Optional["Category"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Category.id"}
    )

    # sub_category
    children: List["Category"] = Relationship(
        back_populates="parent", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    businesses: List["Business"] = Relationship(
        back_populates="categories", link_model=BusinessCategory
    )
    recommendations: List["Recommendation"] = Relationship(
        back_populates="categories", link_model=RecommendationCategory
    )


class CategoryCreate(SchemaBase):
    name: str
    parent_id: Optional[int] = None


class CategoryUpdate(SchemaBase):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class SubCategory(CategoryBase):
    id: int


class CategoryRead(CategoryBase):
    id: int
    children: List[SubCategory] = []


class CategoryIDRead(CategoryBase):
    id: int
