import pytest
from app import create_app
from rfactorapp.database import db


@pytest.fixture
def app():
    app = create_app()
    mongo = db.get_db()
    return app

@pytest.fixture(autouse=True)
def database():
    mongo = db.get_db()
    print('mongo')
    yield mongo
