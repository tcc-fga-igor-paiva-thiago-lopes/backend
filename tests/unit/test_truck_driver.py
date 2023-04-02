import pytest
import sqlalchemy
from src.model.truck_driver import TruckDriver


def test_creation(app):
    with app.app_context():
        truck_driver = TruckDriver.create(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )

        assert truck_driver.id == 1
        assert truck_driver.email == 'jao@mail.com'


def test_duplicated_email(app):
    with app.app_context():
        TruckDriver.create(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )

        with pytest.raises(sqlalchemy.exc.IntegrityError):
            TruckDriver.create(
                name='João',
                email='jao@mail.com',
                password='password',
                password_confirmation='password'
            )


def test_verify_user_password(app):
    with app.app_context():
        truck_driver = TruckDriver.create(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )

        assert not truck_driver.verify_password("12345678")
        assert truck_driver.verify_password("password")


def test_creation_with_different_password(app):
    with app.app_context():
        with pytest.raises(Exception) as error:
            TruckDriver.create(
                name='João',
                email='jao@mail.com',
                password='password',
                password_confirmation='12345678'
            )

        assert str(error.value) == "Password and password confirmation must be equal"
