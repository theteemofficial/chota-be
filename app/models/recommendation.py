from pydantic.networks import EmailStr
from sqlmodel import Field, Relationship, Column, TEXT
from .recommendation_category import RecommendationCategory
from .recommendation_image import RecommendationImageCreate, RecommendationImageRead
from .category import CategoryRead
from .business import BusinessStatus
from typing import Optional, List, TYPE_CHECKING
from datetime import time

from .base import ModelBase, SchemaBase

if TYPE_CHECKING:
    from .recommendation_image import RecommendationImage
    from .category import Category


class RecommendationBase(ModelBase):
    name: str = Field(index=True)
    email: EmailStr = Field(index=True)
    description: str = Field(sa_column=Column(TEXT))
    address: str = Field(index=True)
    phone: str
    cover_image: str
    business_logo: str
    website: Optional[str] = Field(nullable=True)
    facebook: Optional[str] = Field(nullable=True)
    instagram: Optional[str] = Field(nullable=True)
    twitter: Optional[str] = Field(nullable=True)
    linkedin: Optional[str] = Field(nullable=True)
    youtube: Optional[str] = Field(nullable=True)
    open_time: time
    close_time: time
    always_open: Optional[bool] = Field(default=False)
    recommender_email: EmailStr = Field(index=True)


class Recommendation(RecommendationBase, table=True):
    status: BusinessStatus = Field(default=BusinessStatus.pending)
    images: List["RecommendationImage"] = Relationship(back_populates="recommendation")
    categories: List["Category"] = Relationship(
        back_populates="recommendations", link_model=RecommendationCategory
    )


class RecommendationCreate(RecommendationBase):
    category_ids: List[int]
    images: List[RecommendationImageCreate]


class RecommendationUpdate(SchemaBase):
    category_ids: Optional[List[int]] = None
    images: Optional[List[str]] = None
    name: Optional[str] = None
    email: EmailStr = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    cover_image: Optional[str] = None
    business_logo: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    youtube: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    always_open: Optional[bool] = None
    recommender_email: EmailStr = Field(index=True)


class RecommendationRead(RecommendationBase):
    id: int
    categories: List[CategoryRead]
    images: List[RecommendationImageRead]
