import pytest
from src.app import create_app, db


@pytest.fixture()
def app():
    app = create_app(is_testing=True)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here

    # delete everything from database (??)
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def app_ctx(app):
    with app.app_context():
        yield
