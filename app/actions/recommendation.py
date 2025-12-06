from sqlmodel import Session, select
from app.models import (
    RecommendationCreate,
    Recommendation,
    RecommendationCategory,
    RecommendationImage,
)
from typing import Optional


class RecommendationAction:
    """Recommendation-Business-related operations."""

    def create_recommendation(
        self, session: Session, data: RecommendationCreate
    ) -> Optional[Recommendation]:
        new_recommendation = Recommendation(
            name=data.name,
            email=data.email,
            description=data.description,
            address=data.address,
            phone=data.phone,
            cover_image=data.cover_image,
            business_logo=data.business_logo,
            website=data.website,
            facebook=data.facebook,
            instagram=data.instagram,
            twitter=data.twitter,
            linkedin=data.linkedin,
            youtube=data.youtube,
            open_time=data.open_time,
            close_time=data.close_time,
            always_open=data.always_open,
            recommender_email=data.recommender_email,
        )

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


recommendation_action = RecommendationAction()
