from fastapi.testclient import TestClient
from sqlmodel import Session
from app.actions import recommendation_action as ra
from app.core.config import settings
from app.tests.api.api_v1.endpoints.admin.test_auth import test_admin_login_success
from app.models import RecommendationRead


def test_get_all_recommendations(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    recommendation = ra.create_random(session=db_session, data=ra.random())

    response = client.get(f"{settings.API_V1_STR}/admin/recommendation/", headers=headers)
    json = response.json()

    assert response.status_code == 200
    assert json == [RecommendationRead.from_orm(recommendation).jsond()]


def test_get_recommnedation_by_id(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    recommendation = ra.create_random(session=db_session, data=ra.random())

    response = client.get(
        f"{settings.API_V1_STR}/admin/recommendation/{recommendation.id}", headers=headers
    )
    json = response.json()

    assert response.status_code == 200
    assert json == RecommendationRead.from_orm(recommendation).jsond()


def test_get_recommnedation_by_id_not_found(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)

    response = client.get(f"{settings.API_V1_STR}/admin/recommendation/1000", headers=headers)
    json = response.json()

    assert response.status_code == 404
    assert json["detail"] == "Recommendation not found"
