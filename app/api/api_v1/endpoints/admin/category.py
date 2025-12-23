from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List, Optional, Any
from sqlmodel import Session
from app.api import deps, rbac

from app.actions import category_action as ca

from app.models import CategoryRead, AccountRole, CategoryCreate, CategoryUpdate, Category

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.get("/", response_model=List[CategoryRead])
def get_all_category(
    session: CommonSession,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
) -> List[Category]:
    """
    Endpoint for admin to get all category
    """
    return ca.get_all(session)


@router.get("/{id}", response_model=CategoryRead)
def get_category(
    id: int,
    session: CommonSession,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
) -> Category:
    """
    Endpoint for admin to get a category by id
    """
    category = ca.get_by_id(session, id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.post("/", response_model=CategoryRead)
def create_category(
    data: CategoryCreate,
    session: CommonSession,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
) -> Category:
    """
    Endpoint for an admin to create category
    """

    if data.parent_id is not None:
        parent = session.get(Category, data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=404, detail=f"Parent category with id {data.parent_id} does not exist."
            )
    existed_category = ca.get_by_name_and_parent_id(
        session=session, name=data.name, parent_id=data.parent_id
    )
    if existed_category:
        raise HTTPException(status_code=409, detail="Category with this name already exist")
    return ca.create_category(session=session, data=data)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    *,
    session: CommonSession,
    category_id: int,
    category: Optional[CategoryUpdate],
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
) -> Any:
    """
    Update a catgeory by id.
    """
    existing_category = ca.get_by_id(session=session, category_id=category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category with this id does not exist.")
    return ca.update_category(session=session, category_id=category_id, update_data=category)


@router.delete("/{category_id}")
def delete_category(
    *,
    session: CommonSession,
    category_id: int,
    access: bool = Depends(rbac.AdminRoleCheck(roles=[AccountRole.admin])),
) -> Any:
    """
    delete a catgeory and its sub-categories by id.
    Prevent deletion if category is assigned to any business.
    """
    category = ca.get_by_id(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.businesses:
        raise HTTPException(
            status_code=409,
            detail="Category is assigned to one or more businesses",
        )

    for child in category.children:
        if child.businesses:
            raise HTTPException(
                status_code=409,
                detail="One or more sub-categories are assigned to businesses",
            )

    ca.delete_category(session=session, category=category)

    return {"message": "category and its sub-categories deleted successfully"}
