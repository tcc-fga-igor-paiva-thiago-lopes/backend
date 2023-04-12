import pytest
import sqlalchemy
from src.models.truck_driver import TruckDriver


@pytest.mark.usefixtures("app_ctx")
def test_creation():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    assert truck_driver.id == 1
    assert truck_driver.email == "jao@mail.com"


@pytest.mark.usefixtures("app_ctx")
def test_duplicated_email():
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        TruckDriver.create(
            name="João",
            email="jao@mail.com",
            password="password",
            password_confirmation="password",
        )


@pytest.mark.usefixtures("app_ctx")
def test_verify_user_password():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    assert not truck_driver.verify_password("12345678")
    assert truck_driver.verify_password("password")


@pytest.mark.usefixtures("app_ctx")
def test_creation_with_different_password():
    with pytest.raises(Exception) as error:
        TruckDriver.create(
            name="João",
            email="jao@mail.com",
            password="password",
            password_confirmation="12345678",
        )

    assert str(error.value) == "Password and password confirmation must be equal"


@pytest.mark.usefixtures("app_ctx")
def test_creation_without_password():
    with pytest.raises(Exception) as error:
        TruckDriver(name="João", email="jao@mail.com", password_confirmation="12345678")

    assert str(error.value) == "Password and password confirmation are required"


@pytest.mark.usefixtures("app_ctx")
def test_creation_without_password_confirmation():
    with pytest.raises(Exception) as error:
        TruckDriver(
            name="João",
            email="jao@mail.com",
            password="password",
        )

    assert str(error.value) == "Password and password confirmation are required"
