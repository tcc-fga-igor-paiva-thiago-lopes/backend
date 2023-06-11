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

freight_two_attrs = {
    "identifier": "a9df5d98-23c1-4a2e-90a2-189456eedcd4",
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
def test_freights_list_authorization(client):
    response = client.get("/freights/")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_creation_authorization(client):
    response = client.post(
        "/freights/",
        json={
            **freight_one_attrs,
            "start_date": datetime.isoformat(freight_one_attrs["start_date"]),
        },
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_update_authorization(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver)

    response = client.patch(
        f"/freights/{freight.id}",
        json={
            "cargo": FreightCargoEnum.DANGEROUS_GENERAL,
            "status": FreightStatusEnum.WAITING_UNLOAD,
            "description": "changed?",
        },
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_removal_authorization(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver)

    response = client.delete(f"/freights/{freight.id}")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_show_authorization(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_two_attrs, truck_driver=truck_driver)

    response = client.get(
        f"/freights/{freight.id}",
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_list(client):
    truck_driver_one = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    truck_driver_two = TruckDriver.create(
        name="Carlos",
        email="carlos@mail.com",
        password="password",
        password_confirmation="password",
    )

    other_user_freight = freight_one_attrs.copy()
    other_user_freight["identifier"] = "0d6868a1-7e95-4b3b-bf10-8e4b1e23c85f"

    Freight.create(**other_user_freight, truck_driver=truck_driver_two)

    freights = [
        Freight.create(**freight_one_attrs, truck_driver=truck_driver_one),
        Freight.create(**freight_two_attrs, truck_driver_id=truck_driver_one.id),
    ]

    token = create_access_token(identity=truck_driver_one.id)

    response = client.get("/freights/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == requests.codes.ok

    for idx, freight in enumerate(response.json):
        assert freight["id"] == freights[idx].id
        assert freight["truck_driver_id"] == truck_driver_one.id


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
def test_freights_creation_missing_required_fields(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    response = client.post(
        "/freights/",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json == {
        "errors": {
            "identifier": ["campo obrigatório não informado"],
            "agreed_payment": ["campo obrigatório não informado"],
            "cargo_weight": ["campo obrigatório não informado"],
            "contractor": ["campo obrigatório não informado"],
            "description": ["campo obrigatório não informado"],
            "destination_city": ["campo obrigatório não informado"],
            "destination_state": ["campo obrigatório não informado"],
            "distance": ["campo obrigatório não informado"],
            "origin_city": ["campo obrigatório não informado"],
            "origin_state": ["campo obrigatório não informado"],
        },
        "message": "Falha ao validar frete",
    }


@pytest.mark.usefixtures("app_ctx")
def test_freights_creation_with_invalid_fields(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    response = client.post(
        "/freights/",
        json={
            "identifier": "hs6216shd-23c1-4a2e-90a2-189456eedcd",
            "cargo": "Xablau",
            "status": "Unknown status",
            "description": 123,
            "contractor": 456,
            "cargo_weight": "",
            "agreed_payment": "8000",
            "distance": "",
            "start_date": "2023-05-",
            "due_date": "2023-05-",
            "finished_date": "2023-05-",
            "origin_city": 567,
            "origin_state": "BRA",
            "origin_country": 567,
            "origin_latitude": "",
            "origin_longitude": "",
            "destination_city": 789,
            "destination_state": "BRA",
            "destination_country": 789,
            "destination_latitude": "",
            "destination_longitude": "",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json == {
        "errors": {
            "cargo": [
                "Deve ser uma das seguintes opções: Geral, Conteinerizada, Frigorificada, Granel Líquido, "
                + "Granel Pressurizada, Granel Sólido, Neogranel, Perigosa Geral, Perigosa Conteinerizada, "
                + "Perigosa Frigorificada, Perigosa Granel Líquido, Perigosa Granel Pressurizada, "
                + "Perigosa Granel Sólido."
            ],
            "cargo_weight": ["Não é um número válido"],
            "contractor": ["Não é uma string (texto) válido"],
            "description": ["Não é uma string (texto) válido"],
            "destination_city": ["Não é uma string (texto) válido"],
            "destination_country": ["Não é uma string (texto) válido"],
            "destination_latitude": ["Não é um número válido"],
            "destination_longitude": ["Não é um número válido"],
            "destination_state": ["Maior que o tamanho máximo de 2 caracteres"],
            "distance": ["Não é um número válido"],
            "due_date": ["Não é uma data e hora válida"],
            "finished_date": ["Não é uma data e hora válida"],
            "origin_city": ["Não é uma string (texto) válido"],
            "origin_country": ["Não é uma string (texto) válido"],
            "origin_latitude": ["Não é um número válido"],
            "origin_longitude": ["Não é um número válido"],
            "origin_state": ["Maior que o tamanho máximo de 2 caracteres"],
            "start_date": ["Não é uma data e hora válida"],
            "status": [
                "Deve ser uma das seguintes opções: Não iniciado, Em progresso, Aguardando descarga, Finalizado."
            ],
        },
        "message": "Falha ao validar frete",
    }


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
def test_freights_update_not_found(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    response = client.patch(
        "/freights/1289371892371823123",
        json={
            "cargo": FreightCargoEnum.DANGEROUS_GENERAL,
            "status": FreightStatusEnum.WAITING_UNLOAD,
            "description": "changed?",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.not_found


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


@pytest.mark.usefixtures("app_ctx")
def test_freights_removal_not_found(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    response = client.delete(
        "/freights/9817283123812312",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.not_found


@pytest.mark.usefixtures("app_ctx")
def test_freights_show(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    freight = Freight.create(**freight_two_attrs, truck_driver=truck_driver)

    token = create_access_token(identity=truck_driver.id)

    response = client.get(
        f"/freights/{freight.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.ok

    assert response.json["cargo"] == freight_two_attrs["cargo"]
    assert response.json["status"] == freight_two_attrs["status"]
    assert response.json["description"] == freight_two_attrs["description"]


@pytest.mark.usefixtures("app_ctx")
def test_freights_show_not_found(client):
    truck_driver = TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    token = create_access_token(identity=truck_driver.id)

    response = client.get(
        "/freights/12381273612837861",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.not_found
