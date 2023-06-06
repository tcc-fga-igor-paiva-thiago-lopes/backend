import pytest
import requests
from dateutil import parser
from datetime import datetime
from werkzeug.exceptions import NotFound
from flask_jwt_extended import create_access_token

from src.app import db
from src.models.truck_driver import TruckDriver
from src.models.freight import Freight, FreightCargoEnum, FreightStatusEnum


freight_one_attrs = {
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

freight_two_attrs = {
    "cargo": FreightCargoEnum.GENERAL,
    "status": FreightStatusEnum.NOT_STARTED,
    "description": "there and back again 2",
    "contractor": "Jefferson Caminhões",
    "cargo_weight": 2.5,
    "agreed_payment": 3400.09,
    "distance": 2177.25,
    "start_date": parser.parse("2023-05-29T16:30:00.000Z"),
    "origin_city": "Brasília",
    "origin_state": "DF",
    "destination_city": "São Paulo",
    "destination_state": "SP",
}


@pytest.mark.usefixtures("app_ctx")
def test_freights_list(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freights = [
        Freight.create(**freight_one_attrs, truck_driver=truck_driver),
        Freight.create(**freight_two_attrs, truck_driver_id=truck_driver.id),
    ]

    token = create_access_token(identity=truck_driver.id)

    response = client.get("/freights/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == requests.codes.ok

    for idx, freight in enumerate(response.json):
        assert freight["id"] == freights[idx].id
        assert freight["truck_driver_id"] == freights[idx].truck_driver.id


@pytest.mark.usefixtures("app_ctx")
def test_freights_creation(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    assert len(truck_driver.freights) == 0

    response = client.post(
        "/freights/",
        json={
            **freight_one_attrs,
            "start_date": datetime.isoformat(freight_one_attrs["start_date"]),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    truck_driver.reload()

    assert response.status_code == requests.codes.created
    assert len(truck_driver.freights) == 1


@pytest.mark.usefixtures("app_ctx")
def test_freights_update(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver)

    token = create_access_token(identity=truck_driver.id)

    response = client.patch(
        f"/freights/{freight.id}",
        json={
            "cargo": FreightCargoEnum.DANGEROUS_GENERAL,
            "status": FreightStatusEnum.WAITING_UNLOAD,
            "description": "changed?",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.ok

    freight.reload()

    assert freight.cargo == FreightCargoEnum.DANGEROUS_GENERAL
    assert freight.status == FreightStatusEnum.WAITING_UNLOAD
    assert freight.description == "changed?"


@pytest.mark.usefixtures("app_ctx")
def test_freights_removal(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver)

    token = create_access_token(identity=truck_driver.id)

    response = client.delete(
        f"/freights/{freight.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.no_content

    with pytest.raises(NotFound):
        db.get_or_404(Freight, freight.id)
