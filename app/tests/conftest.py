import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.main import app

from dotenv import load_dotenv

from app.api.deps import get_session


load_dotenv()

TEST_DATABASE_URL = "sqlite:///./tmp/test.db"


@pytest.fixture(scope="session")
def engine():
    """Create a single database engine for the whole test session."""
    test_db_path = "./tmp/test.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)  # Create tables
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Creates a new database session for each test.
    The tables persist within the same engine.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    yield TestClient(app)
    del app.dependency_overrides[get_session]
