from fastapi.testclient import TestClient


def test_history(client: TestClient) -> None:
    response = client.get("api/v1/rpn/history")
    assert response.status_code == 200

    response = client.get("api/v1/rpn/history?skip=3&limit=5")
    assert response.status_code == 200


def test_calculate(client: TestClient) -> None:
    expression = ""

    response = client.post("api/v1/rpn/evaluate", json={"expression": expression})
    assert response.status_code == 201


def test_export(client: TestClient) -> None:
    response = client.get("api/v1/rpn/history/export")
    assert response.status_code == 200
