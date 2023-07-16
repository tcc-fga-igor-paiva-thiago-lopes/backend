import pytz
import pytest
import sqlalchemy
from dateutil import parser
from datetime import datetime, timedelta

from src.models.freight import Freight, FreightCargoEnum, FreightStatusEnum
from src.models.category import Category
from src.models.account import Account

freight_attrs = {
    "identifier": "a9df5d98-23c1-4a2e-90a2-189456eedcd3",
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
def test_creation(truck_driver_one):
    freight = Freight.create(**freight_attrs, truck_driver=truck_driver_one)
    category = Category.create(
        identifier="as8273-23c1-4a2e-90a2-189456eedcd3",
        name="Fuel",
        color="#ffffff",
        truck_driver=truck_driver_one,
    )

    account = Account.create(
        freight=freight,
        category=category,
        name="water",
        value=5.5,
        identifier="as8273-66c2-4a2e-90a2-189456eedcd3",
        account_date=datetime.now(pytz.timezone("UTC")),
        description="description",
    )

    datetime_now = datetime.now(pytz.timezone("UTC"))

    assert account.id == 1
    assert account.name == "water"
    assert account.updated_at is None
    assert abs(datetime_now - account.created_at.replace(tzinfo=pytz.UTC)) < timedelta(
        minutes=1
    )
    assert account.freight == freight
    assert account.category == category
    assert account.truck_driver == truck_driver_one


@pytest.mark.usefixtures("app_ctx")
def test_creation_without_freight(truck_driver_one):
    category = Category.create(
        identifier="as8273-23c1-4a2e-90a2-189456eedcd3",
        name="Fuel",
        color="#ffffff",
        truck_driver=truck_driver_one,
    )

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        Account.create(
            category=category,
            name="water",
            value=5.5,
            account_date=datetime.now(pytz.timezone("UTC")),
            description="description",
        )


@pytest.mark.usefixtures("app_ctx")
def test_creation_without_category(truck_driver_one):
    freight = Freight.create(**freight_attrs, truck_driver=truck_driver_one)

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        Account.create(
            freight=freight,
            name="water",
            value=5.5,
            account_date=datetime.now(pytz.timezone("UTC")),
            description="description",
        )
