import pytest
import requests
from flask_jwt_extended import decode_token
from src.models.truck_driver import TruckDriver


@pytest.mark.usefixtures("app_ctx")
def test_login_success(app, client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"email": "jao@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.ok

    assert decode_token(response.json["token"])["sub"] == 1


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_wrong_password(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"email": "jao@mail.com", "password": "passwordd"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.unauthorized
    assert response.json["message"] == "Usuário ou senha incorretos"


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_email_not_registered(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"email": "jaoo@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.not_found
    assert (
        response.json["message"]
        == f'Usuário com e-mail {params["email"]} não encontrado'
    )


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_missing_password(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"email": "jao@mail.com"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Os seguintes campos são obrigatórios: senha"


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_missing_email(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Os seguintes campos são obrigatórios: e-mail"


@pytest.mark.usefixtures("app_ctx")
def test_user_authentication(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {"email": "jao@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    token = response.json["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/truck-drivers/authenticated", headers=headers)

    assert response.status_code == requests.codes.ok
    assert response.json["id"] == 1


@pytest.mark.usefixtures("app_ctx")
def test_user_authentication_fail(client):
    response = client.get("/truck-drivers/authenticated")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_creation_with_duplicated_email(client):
    TruckDriver.create(
        name="João",
        email="jao@mail.com",
        password="password",
        password_confirmation="password",
    )

    params = {
        "name": "Carlos",
        "email": "jao@mail.com",
        "password": "123",
        "password_confirmation": "123",
    }

    response = client.post("/truck-drivers/", json=params)

    assert response.status_code == requests.codes.unprocessable_entity
    assert response.json["message"] == "Email já cadastrado"
