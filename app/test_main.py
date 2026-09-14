# app/test_main.py
import main


def test_health():
    client = main.app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_metrics():
    client = main.app.test_client()
    response = client.get("/metrics")

    assert response.status_code == 200


def test_create_and_list_item():
    client = main.app.test_client()

    # create an item
    response = client.post("/items", json={"id": "1", "name": "test-item"})
    assert response.status_code == 201

    # verify it appears in the list
    response = client.get("/items")
    assert response.status_code == 200
    items = response.get_json()
    assert {"id": "1", "name": "test-item"} in items
