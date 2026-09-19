import main

def test_health():
    client = main.app.test_client()
    response = client.get("/data/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "dataapp"

def test_data_report():
    client = main.app.test_client()
    response = client.get("/data/report")
    assert response.status_code == 200
    data = response.get_json()
    assert data["team"] == "data"
