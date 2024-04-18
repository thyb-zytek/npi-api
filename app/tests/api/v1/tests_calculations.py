import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from models import Calculation
from tools.rpn_calculator import OPERATORS, VARIABLES


def test_helper(client: TestClient) -> None:
    response = client.get("api/v1/rpn/helper")
    assert response.status_code == 200
    assert response.json() == {"operators": [{"name": value[2], "symbol": key} for key, value in OPERATORS.items()],
                               "variables": [{"name": value[1], "symbol": key} for key, value in VARIABLES.items()]}


@pytest.mark.parametrize('expressions', [10], indirect=True)
def test_history(expressions: list[Calculation], client: TestClient) -> None:
    response = client.get("api/v1/rpn/history")
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 10
    assert content["data"] == [expression.model_dump(mode="json") for expression in expressions]

    response = client.get("api/v1/rpn/history?skip=3&limit=5")
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 10
    assert len(content["data"]) == 5
    assert content["data"] == [expression.model_dump(mode="json") for expression in expressions[3:(3 + 5)]]


@pytest.mark.parametrize('expression, expected', [
    pytest.param('2 3 ^', 8),
    pytest.param('10 3 /', 3.3333333333),
    pytest.param('0.94 asin', 1.2226303055),
    pytest.param('2 3 + 4 ^ 5 *', 3125),
])
def test_calculate(expression, expected, client: TestClient) -> None:
    response = client.post("api/v1/rpn/evaluate", json={"expression": expression})
    assert response.status_code == 201
    assert response.json()["result"] == expected


@pytest.mark.parametrize('expressions', [1], indirect=True)
def test_read_calculation(expressions: list[Calculation], client: TestClient) -> None:
    response = client.get(f"api/v1/rpn/history/{expressions[0].id}")
    assert response.status_code == 200
    assert response.json() == expressions[0].model_dump(mode='json')


def test_read_calculation_not_existing(client: TestClient) -> None:
    response = client.get("api/v1/rpn/history/999")
    assert response.status_code == 404


@pytest.mark.parametrize('expressions', [1], indirect=True)
def test_update_calculation(expressions: list[Calculation], client: TestClient, db: Session) -> None:
    assert expressions[0].updated_at is None

    response = client.patch(f"api/v1/rpn/history/{expressions[0].id}", json={'expression': "2 10 *"})

    assert response.status_code == 200
    content = response.json()
    assert content["result"] == 20
    updated_date = content["updated_at"]

    db.refresh(expressions[0])
    assert expressions[0].updated_at.isoformat(timespec="microseconds").replace("+00:00", "Z") == updated_date


def test_update_calculation_not_existing(client: TestClient) -> None:
    response = client.patch("api/v1/rpn/history/999", json={'expression': "2 10 *"})
    assert response.status_code == 404
