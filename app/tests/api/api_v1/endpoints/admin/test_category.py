from fastapi.testclient import TestClient
from sqlmodel import Session
from app.actions import category_action as ca
from app.core.config import settings
from app.tests.api.api_v1.endpoints.admin.test_auth import test_admin_login_success
from app.models import CategoryRead


def test_get_all_categories(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    category = ca.create_random(session=db_session, data=ca.random())
    response = client.get(
        f"{settings.API_V1_STR}/admin/category/",
        headers=headers,
    )
    json = response.json()
    assert response.status_code == 200
    assert json == [CategoryRead.from_orm(category).jsond()]


def test_get_category_by_id(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    category = ca.create_random(db_session)

    response = client.get(
        f"{settings.API_V1_STR}/admin/category/{category.id}",
        headers=headers,
    )
    json = response.json()
    assert response.status_code == 200
    assert json["name"] == category.name
    assert json == CategoryRead.from_orm(category).jsond()


def test_get_category_not_found(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)

    response = client.get(
        f"{settings.API_V1_STR}/admin/category/10000",
        headers=headers,
    )
    json = response.json()
    assert response.status_code == 404
    assert "Category not found" in json["detail"]


def test_create_category_success(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    data = ca.random()

    response = client.post(
        f"{settings.API_V1_STR}/admin/category/", headers=headers, json=data.jsond()
    )
    json = response.json()
    assert response.status_code == 200
    assert json["name"] == data.name
    assert json["parent_id"] == data.parent_id
    assert "id" in json


def test_create_category_parent_id_does_not_exist(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    data = ca.random(parent_id=9)

    response = client.post(
        f"{settings.API_V1_STR}/admin/category/", headers=headers, json=data.jsond()
    )
    json = response.json()
    assert response.status_code == 404
    assert f"Parent category with id {data.parent_id} does not exist." in json["detail"]


def test_create_category_already_exist(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    existing_category = ca.create_random(session=db_session, data=ca.random(name="Food"))

    data = ca.random(name=existing_category.name)

    response = client.post(
        f"{settings.API_V1_STR}/admin/category/", headers=headers, json=data.jsond()
    )
    json = response.json()
    assert response.status_code == 409
    assert "Category with this name already exist" in json["detail"]


def test_create_category_unauthenticated_fails(client: TestClient, db_session: Session):
    data = ca.random(name="Books", parent_id=None)

    response = client.post(
        f"{settings.API_V1_STR}/admin/category/",
        json=data.jsond(),
    )

    assert response.status_code == 401


def test_update_category_success(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    category = ca.create_random(session=db_session, data=ca.random(name="Food"))

    update_data = ca.random(name="UpdateFood")

    response = client.put(
        f"{settings.API_V1_STR}/admin/category/{category.id}",
        headers=headers,
        json=update_data.jsond(),
    )
    json = response.json()
    assert response.status_code == 200
    assert json["id"] == category.id
    assert json["name"] == update_data.name


def test_update_category_does_not_exist(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)
    update_data = ca.random(name="No category ")
    response = client.put(
        f"{settings.API_V1_STR}/admin/category/1000", headers=headers, json=update_data.jsond()
    )
    json = response.json()
    assert response.status_code == 404
    assert json["detail"] == "Category with this id does not exist."


def test_update_category_unauthenticated(client: TestClient, db_session: Session):
    category = ca.create_category(
        session=db_session,
        data=ca.random(name="Books", parent_id=None),
    )

    update_data = ca.random(name="Updated")

    response = client.put(
        f"{settings.API_V1_STR}/admin/category/{category.id}",
        json=update_data.jsond(),
    )

    assert response.status_code == 401


def test_delete_category_success(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)

    category = ca.create_random(db_session)

    response = client.delete(
        f"{settings.API_V1_STR}/admin/category/{category.id}",
        headers=headers,
    )
    json = response.json()
    assert response.status_code == 200
    assert json["message"] == "category and its sub-categories deleted successfully"


def test_delete_category_unauthenticated(client: TestClient, db_session: Session):
    category = ca.create_random(db_session)

    response = client.delete(
        f"{settings.API_V1_STR}/admin/category/{category.id}",
    )
    assert response.status_code == 401


def test_delete_category_not_found_fails(client: TestClient, db_session: Session):
    headers = test_admin_login_success(client, db_session)

    response = client.delete(
        f"{settings.API_V1_STR}/admin/category/99999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


# complete when business action is ready

# def test_delete_category_assigned_to_business_fails(
#     client: TestClient, db_session: Session
# ):
#     headers = test_admin_login_success(client, db_session)

#     category = ca.create_category(
#         session=db_session,
#         data=CategoryCreate(name="Electronics", parent_id=None),
#     )

#     # attach category to a business
#     business = ba.create_random(db_session)
#     business.categories.append(category)
#     db_session.commit()

#     response = client.delete(
#         f"{settings.API_V1_STR}/admin/category/{category.id}",
#         headers=headers,
#     )

#     assert response.status_code == 409
#     assert "assigned to one or more businesses" in response.json()["detail"]


# def test_delete_category_with_child_assigned_to_business_fails(
#     client: TestClient, db_session: Session
# ):
#     headers = test_admin_login_success(client, db_session)

#     parent = ca.create_category(
#         session=db_session,
#         data=CategoryCreate(name="Parent", parent_id=None),
#     )

#     child = ca.create_category(
#         session=db_session,
#         data=CategoryCreate(name="Child", parent_id=parent.id),
#     )

#     business = ba.create_random(db_session)
#     business.categories.append(child)
#     db_session.commit()

#     response = client.delete(
#         f"{settings.API_V1_STR}/admin/category/{parent.id}",
#         headers=headers,
#     )

#     assert response.status_code == 409
#     assert "sub-categories" in response.json()["detail"]
