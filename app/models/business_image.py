from .base import ModelBase, SchemaBase
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .business import Business


class BusinessImageBase(ModelBase):
    business_id: int = Field(foreign_key="business.id")
    image: str


class BusinessImage(BusinessImageBase, table=True):
    business: "Business" = Relationship(back_populates="images")


class BusinessImageCreate(SchemaBase):
    images: List[str]


class BusinessImageUpdate(SchemaBase):
    business_id: Optional[int] = None
    image: Optional[str] = None


class BusinessImageRead(BusinessImageBase):
    id: int
