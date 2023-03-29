import pytest
import sqlalchemy
from src.model.truck_driver import TruckDriver


def test_truck_driver_creation(app):
    with app.app_context():
        truck_driver = TruckDriver(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )
        truck_driver.save()

        assert truck_driver.id == 1
        assert truck_driver.email == 'jao@mail.com'


def test_truck_driver_duplicated_email(app):
    with app.app_context():
        truck_driver = TruckDriver(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )
        truck_driver.save()

        with pytest.raises(sqlalchemy.exc.IntegrityError):
            truck_driver = TruckDriver(
                name='João',
                email='jao@mail.com',
                password='password',
                password_confirmation='password'
            )
            truck_driver.save()
