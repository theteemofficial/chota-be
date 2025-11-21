from sqlmodel import Session, select
from app.db.session import engine
from app.models.admin import Admin
from app.core.config import settings
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_admin():
    with Session(engine) as session:
        admin_exists = session.exec(
            select(Admin).where(Admin.email == settings.FIRST_SUPERUSER)
        ).first()
        if admin_exists:
            logger.info("Admin already exists.")
            return

        admin = Admin(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        session.add(admin)
        session.commit()
        logger.info("Admin seeded successfully!")
