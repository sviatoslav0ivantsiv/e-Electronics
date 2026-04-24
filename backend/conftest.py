import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app  # works because pythonpath = src

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_cursor():
    with patch("database.core.get_connection") as mock_conn:
        cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = cursor
        yield cursor

@pytest.fixture
def fake_user():
    return {"id": 1, "email": "alice@example.com", "role": "user"}

@pytest.fixture(autouse=True)
def disable_rate_limiter():
    yield
    app.state.limiter._storage.reset()