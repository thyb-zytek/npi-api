from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, create_engine

from alembic.command import upgrade
from alembic.config import Config
from core.config import Settings
from core.dependencies import get_db
from main import app
from models import SQLModel

settings = Settings(POSTGRES_DB="test")
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
TestSession = Session(engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """Session for SQLAlchemy."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(db) -> Generator[TestClient, None, None]:
    def get_test_db():
        return db

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as client:
        yield client


def pytest_configure(config):
    db_uri = str(settings.SQLALCHEMY_DATABASE_URI)
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)

    with engine.begin() as connection:
        config = Config("alembic.ini")
        if connection is not None:
            config.attributes['connection'] = connection
        upgrade(config, "head")

    SQLModel.metadata.create_all(engine)
