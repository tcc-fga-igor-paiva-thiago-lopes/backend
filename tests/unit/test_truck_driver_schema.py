import pytest

from src.app import db
from src.models.truck_driver import TruckDriver
from src.schemas.truck_driver_schema import truck_driver_schema, truck_drivers_schema


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_load_with_id():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    ret = truck_driver_schema.load(truck_driver.id)

    assert isinstance(ret, TruckDriver)
    assert ret.id == truck_driver.id


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_load():
    truck_driver_attrs = {
        "name": "João",
        "email": "jao@mail.com",
        "password": "password",
        "password_confirmation": "password",
    }

    truck_driver = truck_driver_schema.load(truck_driver_attrs)

    assert isinstance(truck_driver, TruckDriver)
    assert truck_driver.id is None

    truck_driver.save()

    assert truck_driver.id is not None


@pytest.mark.usefixtures("app_ctx")
def test_truck_driver_dump():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    td_dict = truck_driver_schema.dump(truck_driver)

    assert td_dict["id"] == truck_driver.id
    assert td_dict["email"] == truck_driver.email
    assert td_dict["last_sign_in_at"] is None
    assert td_dict["created_at"] == truck_driver.created_at.isoformat()
    assert td_dict["updated_at"] == truck_driver.updated_at.isoformat()


@pytest.mark.usefixtures("app_ctx")
def test_truck_drivers_load():
    truck_drivers_attrs = [
        {
            "name": "João",
            "email": "jao@mail.com",
            "password": "123",
            "password_confirmation": "123",
        },
        {
            "name": "John",
            "email": "john@mail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    ]

    truck_drivers = truck_drivers_schema.load(truck_drivers_attrs)

    assert isinstance(truck_drivers[0], TruckDriver)
    assert truck_drivers[0].id is None
    assert truck_drivers[0].email == "jao@mail.com"

    assert isinstance(truck_drivers[1], TruckDriver)
    assert truck_drivers[1].id is None
    assert truck_drivers[1].email == "john@mail.com"

    truck_drivers[1].save()

    assert truck_drivers[1].id is not None


@pytest.mark.usefixtures("app_ctx")
def test_truck_drivers_dump():
    td_one = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )
    td_two = TruckDriver.create(
        name="John",
        email="john@mail.com",
        password="password",
        password_confirmation="password",
    )

    truck_drivers_dicts = truck_drivers_schema.dump(
        db.session.execute(db.select(TruckDriver).order_by(TruckDriver.id)).scalars()
    )

    expected_pairs = [
        (td_one, truck_drivers_dicts[0]),
        (td_two, truck_drivers_dicts[1]),
    ]

    for data in expected_pairs:
        td, td_dict = data

        assert td_dict["id"] == td.id
        assert td_dict["email"] == td.email
        assert td_dict["last_sign_in_at"] is None
        assert td_dict["created_at"] == td.created_at.isoformat()
        assert td_dict["updated_at"] == td.updated_at.isoformat()
