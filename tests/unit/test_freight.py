import pytz
import pytest
import sqlalchemy
from dateutil import parser
from datetime import datetime, timedelta

from src.models.truck_driver import TruckDriver
from src.models.freight import Freight, FreightCargoEnum, FreightStatusEnum

freight_attrs = {
    "cargo": FreightCargoEnum.NEW_BULK,
    "status": FreightStatusEnum.STARTED,
    "description": "there and back again",
    "contractor": "Jefferson Caminhões",
    "cargo_weight": 18.5,
    "agreed_payment": 8000,
    "distance": 2677.33,
    "start_date": parser.parse("2023-05-24T16:30:00.000Z"),
    "origin_city": "São Paulo",
    "origin_state": "SP",
    "destination_city": "Brasília",
    "destination_state": "DF",
}


@pytest.mark.usefixtures("app_ctx")
def test_creation():
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="12345678",
        password_confirmation="12345678",
    )

    freight = Freight.create(**freight_attrs, truck_driver=truck_driver)

    datetime_now = datetime.now(pytz.timezone("UTC"))

    assert freight.id == 1
    assert freight.cargo == FreightCargoEnum.NEW_BULK
    assert freight.updated_at is None
    assert abs(datetime_now - freight.created_at.replace(tzinfo=pytz.UTC)) < timedelta(
        minutes=1
    )
    assert freight.truck_driver == truck_driver


@pytest.mark.usefixtures("app_ctx")
def test_creation_without_truck_driver():
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        Freight.create(**freight_attrs)
