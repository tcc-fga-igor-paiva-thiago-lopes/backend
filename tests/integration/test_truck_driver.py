from src.model.truck_driver import TruckDriver


login_required_request_params = {
    "email": "",
    'password': ""
}


# failing test TODO: fix it

def test_login_success(app):
    with app.app_context():
        TruckDriver.create(
            name='João',
            email='jao@mail.com',
            password='password',
            password_confirmation='password'
        )
        login_success_params = login_required_request_params.copy()

        login_success_params['email'] = 'jao@mail.com'
        login_success_params['password'] = 'password'

        response = app.post("/truck-drivers/login", json=login_success_params)

        assert response.json is not None
