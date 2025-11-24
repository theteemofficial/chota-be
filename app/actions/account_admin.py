from sqlmodel import Session, select
from app.models import Admin
from typing import Optional
from app.core.security import verify_password


class AdminAction:
    """admin-related account operations."""

    def get_by_email(self, session: Session, email: str) -> Optional[Admin]:
        return session.exec(select(Admin).where(Admin.email == email.lower())).first()

    def authenticate(self, session: Session, *, email: str, password: str) -> Optional[Admin]:
        account = self.get_by_email(session, email=email)
        if (
            not account
            or not verify_password(password, account.hashed_password)
            or not account.is_superuser
        ):
            return None
        return account


admin_action = AdminAction()
