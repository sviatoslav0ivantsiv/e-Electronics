# tests/integration/conftest.py
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from src.auth.controller import require_admin

async def override_require_admin():
    return {"id": 1, "name": "admin", "is_admin": True}

app.dependency_overrides[require_admin] = override_require_admin
client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch("src.auth.service.get_connection") as mock_auth_conn, \
         patch("src.users.service.get_connection") as mock_user_conn, \
         patch("src.products.service.get_connection") as mock_product_conn:
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_auth_conn.return_value = conn
        mock_user_conn.return_value = conn
        mock_product_conn.return_value = conn
        yield conn, cursor