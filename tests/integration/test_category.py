import pytest
import requests

from src.models.category import Category

category_one_attrs = {
    "identifier": "b2de57be-1df9-4d48-a6b3-9a0f58a77d1a",
    "name": "Category One",
    "color": "#000000",
}

category_two_attrs = {
    "identifier": "b2de57be-1df9-4d48-a6b3-9a0f58a77d1b",
    "name": "Category Two",
    "color": "#0000FF",
}

category_three_attrs = {
    "identifier": "b2de57be-1df9-4d48-a6b3-9a0f58a77d1c",
    "name": "Category Three",
    "color": "#00FF00",
}


@pytest.mark.usefixtures("app_ctx")
def test_categories_list_authorization(client):
    response = client.get("/categories/")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_creation_authorization(client):
    response = client.post(
        "/categories/",
        json={
            **category_one_attrs,
        },
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_update_authorization(client, truck_driver_one):
    freight = Category.create(**category_one_attrs, truck_driver=truck_driver_one)

    response = client.patch(
        f"/categories/{freight.id}",
        json={"color": "#FFFFFF"},
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_removal_authorization(client, truck_driver_one):
    freight = Category.create(**category_one_attrs, truck_driver=truck_driver_one)

    response = client.delete(f"/categories/{freight.id}")

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_show_authorization(client, truck_driver_one):
    freight = Category.create(**category_two_attrs, truck_driver=truck_driver_one)

    response = client.get(
        f"/categories/{freight.id}",
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_sync_authorization(client):
    response = client.patch(
        "/categories/",
        json=[category_one_attrs, category_two_attrs],
    )

    assert response.status_code == requests.codes.unauthorized


@pytest.mark.usefixtures("app_ctx")
def test_categories_delete_authorization(client):
    response = client.delete("/categories/")

    assert response.status_code == requests.codes.unauthorized


# TODO: FINISH REMAINING TESTS
