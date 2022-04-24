from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_machine(client: TestClient, random_machine: Dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/machine", json=random_machine)
    machine = response.json()
    assert response.status_code == 200
    assert machine.get("name") == random_machine.get("name")
    assert machine.get("one_coin") == random_machine.get("one_coin")
    assert machine.get("five_coin") == random_machine.get("five_coin")


def test_read_machine(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/machine")
    machine = response.json()
    assert response.status_code == 200
    assert len(machine) > 0


def test_update_machine(client: TestClient, random_machine: Dict[str, str]) -> None:
    random_machine["one_coin"] = 100
    random_machine["one_coin"] = 50
    response = client.put(f"{settings.API_V1_STR}/machine", json=random_machine)
    machine = response.json()
    assert response.status_code == 200
    assert machine.get("name") == random_machine.get("name")
    assert machine.get("one_coin") == random_machine.get("one_coin")
    assert machine.get("five_coin") == random_machine.get("five_coin")


def test_delete_machine(client: TestClient) -> None:
    response = client.delete(f"{settings.API_V1_STR}/machine")
    message = response.json()
    assert response.status_code == 200
    assert "message" in message
