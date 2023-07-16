import pytest
import requests
from flask_jwt_extended import decode_token


@pytest.mark.usefixtures("app_ctx")
def test_login_success(client, truck_driver_one):
    params = {"email": "jao@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.ok

    assert decode_token(response.json["token"])["sub"] == 1
    assert response.json["name"] == "João"


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_wrong_password(client, truck_driver_one):
    params = {"email": "jao@mail.com", "password": "passwordd"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.unauthorized
    assert response.json["message"] == "Usuário ou senha incorretos"


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_email_not_registered(client, truck_driver_one):
    params = {"email": "jaoo@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.not_found
    assert (
        response.json["message"]
        == f'Usuário com e-mail {params["email"]} não encontrado'
    )


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_missing_password(client, truck_driver_one):
    params = {"email": "jao@mail.com"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Os seguintes campos são obrigatórios: senha"


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_missing_email(client, truck_driver_one):
    params = {"password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.bad_request
    assert response.json["message"] == "Os seguintes campos são obrigatórios: e-mail"


@pytest.mark.usefixtures("app_ctx")
def test_user_authentication(client, truck_driver_one):
    params = {"email": "jao@mail.com", "password": "password"}

    response = client.post("/truck-drivers/login", json=params)

    token = response.json["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/truck-drivers/authenticated", headers=headers)

    assert response.status_code == requests.codes.no_content


@pytest.mark.usefixtures("app_ctx")
def test_user_authentication_fail(client):
    response = client.get("/truck-drivers/authenticated")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_creation_with_duplicated_email(client, truck_driver_one):
    params = {
        "name": "Carlos",
        "email": "jao@mail.com",
        "password": "12345678",
        "password_confirmation": "12345678",
    }

    response = client.post("/truck-drivers/", json=params)

    assert response.status_code == requests.codes.unprocessable_entity
    assert response.json["message"] == "Email já cadastrado"
