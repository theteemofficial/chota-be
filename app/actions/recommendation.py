from sqlmodel import Session, select
from app.models import (
    RecommendationCreate,
    Recommendation,
    RecommendationCategory,
    RecommendationImage,
    RecommendationImageCreate,
)
from typing import Optional
from faker import Faker

fake = Faker()


class RecommendationAction:
    """Recommendation-Business-related operations."""

    def create_recommendation(
        self, session: Session, data: RecommendationCreate
    ) -> Optional[Recommendation]:
        new_recommendation = Recommendation(**data.model_dump(exclude={"category_ids", "images"}))

        session.add(new_recommendation)
        session.commit()
        session.refresh(new_recommendation)

        # Save categories
        for cid in data.category_ids:
            session.add(
                RecommendationCategory(recommendation_id=new_recommendation.id, category_id=cid)
            )

            # Save images
        for url in data.images:
            session.add(
                RecommendationImage(recommendation_id=new_recommendation.id, image=url.image)
            )

        session.commit()
        session.refresh(new_recommendation)

        return new_recommendation

    def get_all(self, session: Session) -> list[Recommendation]:
        return session.exec(select(Recommendation)).all()

    def get_by_id(self, session: Session, recommendation_id: int) -> Recommendation:
        recommendation = session.get(Recommendation, recommendation_id)
        return recommendation

    def random(self, **data):
        return RecommendationCreate(
            name=data.get("name", fake.name()),
            email=data.get("email", fake.email()),
            description=data.get("description", fake.text()),
            address=data.get("address", fake.name()),
            phone=data.get("phone", fake.msisdn()),
            cover_image=data.get("cover_image", fake.url()),
            business_logo=data.get("business_logo", fake.text()),
            website=data.get("website", fake.url()),
            facebook=data.get("facebook", fake.url()),
            instagram=data.get("instagram", fake.url()),
            twitter=data.get("twitter", fake.url()),
            linkedin=data.get("linkedin", fake.url()),
            youtube=data.get("youtube", fake.url()),
            open_time=data.get("open_time", fake.time()),
            close_time=data.get("close_time", fake.time()),
            always_open=data.get("always_open", fake.boolean(chance_of_getting_true=70)),
            recommender_email=data.get("recommender_email", fake.email()),
            category_ids=data.get("category_ids", [1]),
            images=data.get("images", [RecommendationImageCreate(image=fake.image_url())]),
        )

    def create_random(self, session: Session, **dict: dict) -> Recommendation:
        return self.create_recommendation(session=session, data=self.random(**dict))


recommendation_action = RecommendationAction()
