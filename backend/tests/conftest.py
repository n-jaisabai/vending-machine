from typing import Dict, Generator

import pytest

from fastapi.testclient import TestClient

from app.database.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def random_product() -> Dict[str, str]:
    return {
        "id": 9999,
        "name": "Test Product",
        "price": 80,
        "stock": 20
    }


@pytest.fixture(scope="module")
def random_machine() -> Dict[str, str]:
    return {
        "id": 9999,
        "name": "Test Machine",
        "one_coin": 50,
        "five_coin": 40,
        "ten_coin": 30,
        "twenty_banknote": 20,
        "fifty_banknote": 25,
        "hundred_banknote": 30,
        "five_hundred_banknote": 10,
        "thousand_banknote": 10,
    }