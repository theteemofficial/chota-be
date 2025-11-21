import logging

from app import models  # noqa: F401
from app.db.init_db import init_db
from app.db.session import Session, engine
from app.seed.seeders import admin


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# for seeding
def init() -> None:
    with Session(engine):
        init_db(engine=engine, create_tables=True)

    # seed admin
    admin.seed_admin()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
