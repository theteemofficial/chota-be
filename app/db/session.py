from sqlmodel import Session, create_engine, pool  # noqa
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if settings.USE_SQLITE:
    engine = create_engine(
        settings.SQLITE_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
        echo=settings.DB_DEBUG_MODE,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DB_DEBUG_MODE,
    )

try:
    with engine.connect() as connection:
        logger.info("Connection successful!")
except Exception as e:
    logger.info(f"Failed to connect: {e}")
