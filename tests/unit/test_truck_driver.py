import pytz
import pytest
import sqlalchemy
from dateutil import parser
from datetime import datetime, timedelta

from src.app import db
from src.models.freight import Freight
from src.models.truck_driver import TruckDriver


@pytest.mark.usefixtures("app_ctx")
def test_creation():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    datetime_now = datetime.now(pytz.timezone("UTC"))

    assert truck_driver.id == 1
    assert truck_driver.email == "jao@mail.com"
    assert truck_driver.updated_at is None
    assert abs(
        datetime_now - truck_driver.created_at.replace(tzinfo=pytz.UTC)
    ) < timedelta(minutes=1)


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


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_partial_update():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="12345678",
        password_confirmation="12345678",
    )

    assert truck_driver.updated_at is None

    truck_driver.update(name="João Silva")

    datetime_now = datetime.now(pytz.timezone("UTC"))

    assert truck_driver.name == "João Silva"
    assert abs(
        datetime_now - truck_driver.updated_at.replace(tzinfo=pytz.UTC)
    ) < timedelta(minutes=1)


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_removal():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="12345678",
        password_confirmation="12345678",
    )

    truck_driver.destroy()

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db.session.execute(
            db.select(TruckDriver).filter_by(email=truck_driver.email)
        ).scalar_one()


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_freights_association():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="12345678",
        password_confirmation="12345678",
    )

    freight = Freight.create(
        cargo="Neogranel",
        status="Em progresso",
        description="there and back again",
        contractor="Jefferson Caminhões",
        cargo_weight=18.5,
        agreed_payment=8000,
        distance=2677.33,
        start_date=parser.parse("2023-05-24T16:30:00.000Z"),
        origin_city="São Paulo",
        origin_state="SP",
        destination_city="Brasília",
        destination_state="DF",
        truck_driver=truck_driver,
    )

    assert freight in truck_driver.freights
