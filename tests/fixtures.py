import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.employees import models
from app.tasks import models
from app.teams import models


@pytest.fixture(name="session")
def session():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session