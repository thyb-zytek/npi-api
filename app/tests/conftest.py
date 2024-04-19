import random
from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, create_engine

from alembic.command import upgrade
from alembic.config import Config
from core.config import Settings
from core.dependencies import get_db
from main import app
from models import Calculation, CalculationPayload, SQLModel

settings = Settings(POSTGRES_DB="test")
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
TestSession = Session(engine)


def expression_factory(size: int = 1) -> list[str]:
    return random.choices(
        [
            "2 5 +",
            "4 1 -",
            "5 2 *",
            "6 3 /",
            "10 4 %",
            "10 3 /",
            "2 3 ^",
            "5 !",
            "9 sqrt",
            "6 3 /",
            "e ln",
            "e 8 ^",
            "100 log",
            "57 cos",
            "0.56 acos",
            "38 sin",
            "0.94 asin",
            "pi tan",
            "68 tan",
            "2 3 2 ^ ^",
            "5 3 ! ^",
            "2 3 ^ 4 ! *",
            "5 sin 2 ^ cos",
            "2 3 + 4 ^ 5 *",
            "3 ! exp ln",
            "pi 2 * 3 / sin 3 ^ exp 15 sqrt log * cos 0.2 / exp",
        ],
        k=size,
    )


@pytest.fixture(scope="function")
def expressions(request: SubRequest, db: Session) -> list[Calculation]:
    history = []
    for expr in expression_factory(request.param):
        calculation = Calculation.model_validate(
            CalculationPayload(
                expression=expr, precision=random.randint(2, 8)
            ).model_dump()
        )
        db.add(calculation)
        db.commit()
        db.refresh(calculation)
        history.append(calculation)
    return history


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """Session for SQLAlchemy."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def get_test_db() -> Session:
        return db

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope="function")
def clean_db(db: Session) -> Generator[None, None, None]:
    try:
        db.delete(Calculation)
        db.commit()
    except Exception:
        db.rollback()
    yield


def pytest_configure(config: pytest.Config) -> None:
    db_uri = str(settings.SQLALCHEMY_DATABASE_URI)
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)

    with engine.begin() as connection:
        alembic_config = Config("alembic.ini")
        if connection is not None:
            alembic_config.attributes["connection"] = connection
        upgrade(alembic_config, "head")

    SQLModel.metadata.create_all(engine)
