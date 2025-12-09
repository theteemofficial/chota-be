from typing import List

from fastapi import Depends, HTTPException

from app.api.deps import get_current_account
from app.models import Admin, AccountRole


class AdminRoleCheck:
    def __init__(self, roles: List[AccountRole]) -> None:
        self.required_roles = roles

    def __call__(self, admin: Admin = Depends(get_current_account)) -> bool:
        if admin.role not in self.required_roles:
            raise HTTPException(status_code=401, detail="Not authorized")
        return True
