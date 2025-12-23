from fastapi.testclient import TestClient
from sqlmodel import Session
from app.actions import category_action as ca, recommendation_action as ra
from app.core.config import settings


def test_recommend_business_success(client: TestClient, db_session: Session):
    category = ca.create_random(session=db_session, data=ca.random(name="Food"))
    data = ra.random(category_ids=[category.id])

    response = client.post(f"{settings.API_V1_STR}/recommendation/", json=data.jsond())
    json = response.json()

    assert response.status_code == 200
    assert json["name"] == data.name
    assert json["email"] == data.email
    assert json["twitter"] == data.twitter
    assert [c["id"] for c in json["categories"]] == data.category_ids


def test_recommend_business_with_no_category(client: TestClient, db_session: Session):
    data = ra.random(category_ids=[])

    response = client.post(f"{settings.API_V1_STR}/recommendation/", json=data.jsond())
    json = response.json()

    assert response.status_code == 400
    assert json["detail"] == "At least one category must be provided"


def test_recommend_business_with_category_not_found(client: TestClient, db_session: Session):
    data = ra.random(category_ids=[1000])

    response = client.post(f"{settings.API_V1_STR}/recommendation/", json=data.jsond())
    assert response.status_code == 404
