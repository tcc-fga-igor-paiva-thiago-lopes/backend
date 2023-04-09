import jwt
import pytest
import requests
from src.model.truck_driver import TruckDriver


login_required_request_params = {
    "email": "",
    'password': ""
}


@pytest.mark.usefixtures("app_ctx")
def test_login_success(app, client):
    TruckDriver.create(
        name='João',
        email='jao@mail.com',
        password='password',
        password_confirmation='password'
    )
    params = login_required_request_params.copy()

    params['email'] = 'jao@mail.com'
    params['password'] = 'password'

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.ok
    assert jwt.decode(response.json['token'], app.config['SECRET_KEY'],
                      algorithms=["HS256"])['truck_driver_id'] == 1


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_wrong_password(client):
    TruckDriver.create(
        name='João',
        email='jao@mail.com',
        password='password',
        password_confirmation='password'
    )
    params = login_required_request_params.copy()

    params['email'] = 'jao@mail.com'
    params['password'] = 'passwordd'

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.unauthorized
    assert response.json['error'] == 'Senha incorreta'


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_email_not_registered(client):
    TruckDriver.create(
        name='João',
        email='jao@mail.com',
        password='password',
        password_confirmation='password'
    )
    params = login_required_request_params.copy()

    params['email'] = 'jaoo@mail.com'
    params['password'] = 'password'

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.not_found
    assert response.json['error'] == f'Usuário com email {params["email"]} não encontrado'


@pytest.mark.usefixtures("app_ctx")
def test_login_fail_missing_required_fields(app, client):
    TruckDriver.create(
        name='João',
        email='jao@mail.com',
        password='password',
        password_confirmation='password'
    )
    params = login_required_request_params.copy()

    params['email'] = 'jaoo@mail.com'
    params.pop('password')

    response = client.post("/truck-drivers/login", json=params)

    assert response.status_code == requests.codes.unprocessable_entity
    assert response.json['error'] == 'Email e senha são obrigatórios'
