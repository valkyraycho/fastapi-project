from fastapi.testclient import TestClient


def test_root(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
