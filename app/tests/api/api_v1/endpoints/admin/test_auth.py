from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.admin import Admin
from app.core.security import get_password_hash
from app.core.config import settings


def seed_admin(session: Session):
    admin = Admin(
        email="admin@example.com",
        hashed_password=get_password_hash("testpassword123"),
        is_superuser=True,
    )
    session.add(admin)
    session.commit()


def test_admin_login_success(client: TestClient, db_session: Session):
    # Seed admin
    seed_admin(db_session)

    payload = {"username": "admin@example.com", "password": "testpassword123"}
    response = client.post(f"{settings.API_V1_STR}/admin/auth/login", data=payload)

    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"
    assert json["account"]["email"] == "admin@example.com"
    token = json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_admin_login_invalid_password(client, db_session):
    seed_admin(db_session)

    payload = {"username": "admin@example.com", "password": "wrongpass"}

    response = client.post(f"{settings.API_V1_STR}/admin/auth/login", data=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password or not an admin"


def test_admin_login_not_superuser(client, db_session):
    user = Admin(
        email="normal@example.com", hashed_password=get_password_hash("12345"), is_superuser=False
    )
    db_session.add(user)
    db_session.commit()

    payload = {"username": "normal@example.com", "password": "12345"}

    response = client.post(f"{settings.API_V1_STR}/admin/auth/login", data=payload)

    assert response.status_code == 400
