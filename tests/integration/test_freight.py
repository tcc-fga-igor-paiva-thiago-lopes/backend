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
    "due_date": None,
    "finished_date": None,
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
    "due_date": None,
    "finished_date": None,
}

freight_three_import_attrs = {
    "identifier": "1d605f22-bbe5-47d9-a437-86e0d08c6e26",
    "cargo": FreightCargoEnum.DANGEROUS_REFRIGERATED,
    "status": FreightStatusEnum.WAITING_UNLOAD,
    "description": "there and back again 3",
    "contractor": "Chico Fretes",
    "cargo_weight": 1.765,
    "agreed_payment": 2301.93,
    "distance": 3050.11,
    "start_date": "2023-05-24T16:30:00.000Z",
    "origin_city": "Palmas",
    "origin_state": "TO",
    "destination_city": "São José dos Campos",
    "destination_state": "SP",
    "due_date": None,
    "finished_date": None,
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
def test_freights_update_authorization(client, truck_driver_one):
    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)

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
def test_freights_removal_authorization(client, truck_driver_one):
    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)

    response = client.delete(f"/freights/{freight.id}")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_show_authorization(client, truck_driver_one):
    freight = Freight.create(**freight_two_attrs, truck_driver=truck_driver_one)

    response = client.get(
        f"/freights/{freight.id}",
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_sync_authorization(client):
    response = client.patch(
        "/freights/",
        json=[freight_one_attrs, freight_two_attrs],
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_delete_authorization(client):
    response = client.delete("/freights/")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_freights_list(client, truck_driver_one):
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
def test_freights_creation(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    assert len(truck_driver_one.freights) == 0

    response = client.post(
        "/freights/",
        json={
            **freight_one_attrs,
            "start_date": datetime.isoformat(freight_one_attrs["start_date"]),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    truck_driver_one.reload()

    assert response.status_code == requests.codes.created
    assert len(truck_driver_one.freights) == 1


@pytest.mark.usefixtures("app_ctx")
def test_freights_creation_missing_required_fields(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

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
def test_freights_creation_with_invalid_fields(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

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
def test_freights_update(client, truck_driver_one):
    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)

    token = create_access_token(identity=truck_driver_one.id)

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
def test_freights_update_not_found(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

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
def test_freights_removal(client, truck_driver_one):
    freight = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)

    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        f"/freights/{freight.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.no_content

    with pytest.raises(NotFound):
        db.get_or_404(Freight, freight.id)


@pytest.mark.usefixtures("app_ctx")
def test_freights_removal_not_found(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        "/freights/9817283123812312",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.not_found


@pytest.mark.usefixtures("app_ctx")
def test_freights_show(client, truck_driver_one):
    freight = Freight.create(**freight_two_attrs, truck_driver=truck_driver_one)

    token = create_access_token(identity=truck_driver_one.id)

    response = client.get(
        f"/freights/{freight.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.ok

    assert response.json["cargo"] == freight_two_attrs["cargo"]
    assert response.json["status"] == freight_two_attrs["status"]
    assert response.json["description"] == freight_two_attrs["description"]


@pytest.mark.usefixtures("app_ctx")
def test_freights_show_not_found(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.get(
        "/freights/12381273612837861",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.not_found


@pytest.mark.usefixtures("app_ctx")
def test_freights_sync_empty_payload(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.patch(
        "/freights/",
        json=[],
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Nenhum registro a sincronizar"


@pytest.mark.usefixtures("app_ctx")
def test_freights_sync_with_invalid_fields(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.patch(
        "/freights/",
        json=[
            {
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
            {
                "identifier": "3d9f724f-aa0d-4cf7-8b75-97653a5ce5b7",
                "cargo": "Unknown",
                "status": "Status desconhecido ",
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
        ],
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json == {
        "message": "Falha ao validar frete",
        "errors": {
            "0": {
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
            "1": {
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
        },
    }


@pytest.mark.usefixtures("app_ctx")
def test_freights_sync_same_fields(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    import_data = [freight_one_attrs.copy(), freight_two_attrs.copy()]

    for key in ["due_date", "finished_date"]:
        del import_data[1][key]

    for attrs in import_data:
        attrs["contractor"] = "Chico Fretes"
        attrs["start_date"] = attrs["start_date"].isoformat()

    assert len(truck_driver_one.freights) == 0

    response = client.patch(
        "/freights/",
        json=import_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert (
        response.json["message"]
        == "Ao sincronizar registros, todos devem possuir os mesmos campos"
    )

    assert len(truck_driver_one.freights) == 0


# TODO: Test database is a SQLite but in production is PostgreSQL, we must handle this
# TODO: SQLalchemy SQLite Datetime only accepts datetime object
# and Marshmallow only accepts string in Datetime. We must to something to fix this
# @pytest.mark.usefixtures("app_ctx")
# def test_freights_sync_success(client, truck_driver_one):
#     freight_one = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)
#     freight_two = Freight.create(**freight_two_attrs, truck_driver=truck_driver_one)

#     token = create_access_token(identity=truck_driver_one.id)

#     import_data = [
#         {
#             **freight_one_attrs,
#             # "start_date": freight_one_attrs["start_date"],
#             "status": FreightStatusEnum.NOT_STARTED,
#         },
#         {
#             **freight_two_attrs,
#             # "start_date": freight_two_attrs["start_date"],
#             "agreed_payment": 6509.15,
#         },
#         freight_three_import_attrs,
#     ]

#     assert len(truck_driver_one.freights) == 2

#     response = client.patch(
#         "/freights/",
#         json=import_data,
#         headers={"Authorization": f"Bearer {token}"},
#     )

#     assert response.json == [attrs["identifier"] for attrs in import_data]
#     assert response.status_code == requests.codes.ok

#     freight_one.reload()
#     freight_two.reload()

#     assert freight_one.status == FreightStatusEnum.NOT_STARTED
#     assert freight_two.agreed_payment == 6509.15

#     assert len(truck_driver_one.freights) == 3

#     freight_three = db.session.execute(
#         db.select(Freight).order_by(Freight.created_at.desc())
#     ).scalars()[-1]

#     assert freight_three.identifier == freight_three_import_attrs["identifier"]


@pytest.mark.usefixtures("app_ctx")
def test_freights_delete_empty_params(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        "/freights/",
        query_string={"identifiers": []},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Nenhum registro a remover"

    response = client.delete(
        "/freights/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Nenhum registro a remover"


@pytest.mark.usefixtures("app_ctx")
def test_freights_delete_all_not_found(client, truck_driver_one):
    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        "/freights/",
        query_string={
            "identifiers": [
                freight_one_attrs["identifier"],
                freight_two_attrs["identifier"],
            ]
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == requests.codes.accepted
    assert response.json["deleted"] == []
    assert (
        response.json["not_exists"].sort()
        == [
            freight_one_attrs["identifier"],
            freight_two_attrs["identifier"],
        ].sort()
    )


@pytest.mark.usefixtures("app_ctx")
def test_freights_delete_completed_success(client, truck_driver_one):
    freight_one = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)
    freight_two = Freight.create(**freight_two_attrs, truck_driver=truck_driver_one)

    freight_three_attrs = freight_three_import_attrs.copy()

    freight_three_attrs["start_date"] = parser.parse(freight_three_attrs["start_date"])

    freight_three = Freight.create(**freight_three_attrs, truck_driver=truck_driver_one)

    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        "/freights/",
        headers={"Authorization": f"Bearer {token}"},
        query_string={
            "identifiers": [freight_one.identifier, freight_three.identifier]
        },
    )

    assert response.status_code == requests.codes.ok
    assert response.json["not_exists"] == []
    assert (
        response.json["deleted"].sort()
        == [
            freight_one.identifier,
            freight_three.identifier,
        ].sort()
    )

    assert not db.session.query(
        db.exists().where(Freight.id == freight_one.id)
    ).scalar()
    assert db.session.query(db.exists().where(Freight.id == freight_two.id)).scalar()
    assert not db.session.query(
        db.exists().where(Freight.id == freight_three.id)
    ).scalar()


@pytest.mark.usefixtures("app_ctx")
def test_freights_delete_partial_success(client, truck_driver_one):
    freight_one = Freight.create(**freight_one_attrs, truck_driver=truck_driver_one)
    freight_two = Freight.create(**freight_two_attrs, truck_driver=truck_driver_one)

    freight_three_attrs = freight_three_import_attrs.copy()

    freight_three_attrs["start_date"] = parser.parse(freight_three_attrs["start_date"])

    freight_three = Freight.create(**freight_three_attrs, truck_driver=truck_driver_one)

    token = create_access_token(identity=truck_driver_one.id)

    response = client.delete(
        "/freights/",
        headers={"Authorization": f"Bearer {token}"},
        query_string={
            "identifiers": [
                freight_one.identifier,
                freight_three.identifier,
                "xablau-123456-78901-23456789",
            ]
        },
    )

    assert response.status_code == requests.codes.accepted
    assert response.json["not_exists"] == ["xablau-123456-78901-23456789"]
    assert (
        response.json["deleted"].sort()
        == [
            freight_one.identifier,
            freight_three.identifier,
        ].sort()
    )

    assert not db.session.query(
        db.exists().where(Freight.id == freight_one.id)
    ).scalar()
    assert db.session.query(db.exists().where(Freight.id == freight_two.id)).scalar()
    assert not db.session.query(
        db.exists().where(Freight.id == freight_three.id)
    ).scalar()
