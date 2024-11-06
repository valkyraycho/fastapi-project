import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def test_client() -> TestClient:
    test_app = FastAPI()
    test_app.router = app.router
    return TestClient(test_app)
