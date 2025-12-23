from sqlmodel import Session, select
from app.models import (
    CategoryCreate,
    Category,
    CategoryUpdate,
)
from typing import Optional
from faker import Faker

fake = Faker()


class CategoryAction:
    """category-related operations."""

    def normalize_name(self, name: str) -> str:
        return name.strip().lower()

    def create_category(self, session: Session, data: CategoryCreate) -> Optional[Category]:
        normalized_name = self.normalize_name(data.name)
        new_category = Category(name=normalized_name, parent_id=data.parent_id)

        session.add(new_category)
        session.commit()
        session.refresh(new_category)

        return new_category

    def get_all(self, session: Session) -> list[Category]:
        return session.exec(select(Category).where(Category.parent_id == None)).all()  # noqa: E711

    def get_by_id(self, session: Session, category_id: int) -> Category:
        return session.get(Category, category_id)

    def get_by_name_and_parent_id(self, session: Session, name: str, parent_id: int) -> Category:
        normalized_name = self.normalize_name(name)
        return session.exec(
            select(Category).where(
                Category.name == normalized_name, Category.parent_id == parent_id
            )
        ).first()

    def update_category(
        self, session: Session, category_id: int, update_data: CategoryUpdate
    ) -> Optional[Category]:
        category = self.get_by_id(session, category_id)

        if not category:
            return None

        update_dict = update_data.dict(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(category, key, value)

        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    def get_by_ids(self, session: Session, ids: list[int]) -> list[Category]:
        return session.query(Category).filter(Category.id.in_(ids)).all()

    def delete_category(self, session: Session, category: Category) -> bool:
        """Delete a category by ID"""
        session.delete(category)
        session.commit()

    def random(self, **data):
        return CategoryCreate(
            name=data.get("name", self.normalize_name(fake.name())), parent_id=data.get("parent_id")
        )

    def create_random(self, session: Session, **dict: dict) -> Category:
        return self.create_category(session=session, data=self.random(**dict))


category_action = CategoryAction()
