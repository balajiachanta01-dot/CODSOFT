from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200


def test_history():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
