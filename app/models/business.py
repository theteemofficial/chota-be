from pydantic.networks import EmailStr
from sqlmodel import Field, Relationship, Column, TEXT
from .business_category import BusinessCategory
from typing import Optional, List, TYPE_CHECKING
from datetime import time

from .cho_enum import BaseEnum
from .base import ModelBase, SchemaBase

if TYPE_CHECKING:
    from .business_image import BusinessImage, BusinessImageCreate, BusinessImageRead
    from .category import Category, CategoryRead


class BusinessStatus(BaseEnum):
    pending = "pending"
    approved = "aprroved"
    rejected = "rejected"


class BusinessBase(ModelBase):
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
    status: BusinessStatus = Field(default=BusinessStatus.pending)


class Business(BusinessBase, table=True):
    images: List["BusinessImage"] = Relationship(back_populates="business")
    categories: List["Category"] = Relationship(
        back_populates="businesses", link_model=BusinessCategory
    )


class BusinessCreate(BusinessBase):
    category_id: List[int]
    sub_category_id: List[int]
    images: List["BusinessImageCreate"]


class BusinessUpdate(SchemaBase):
    category_ids: Optional[List[int]] = None
    sub_category_ids: Optional[List[int]] = None
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
    status: Optional[BusinessStatus] = None


class BusinessRead(BusinessBase):
    id: int
    category: List["CategoryRead"]
    sub_category: List["CategoryRead"]
    images: List["BusinessImageRead"]
