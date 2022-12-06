import pytest

from project import create_app, db
from project.models import Country

@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()
        db.session.add_all([
            Country(name="United States"),
            Country(name="Canada")
        ])
        db.session.commit()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()