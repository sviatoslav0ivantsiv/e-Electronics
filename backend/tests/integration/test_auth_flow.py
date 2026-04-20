import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch("src.auth.service.get_connection") as mock_conn, \
         patch("src.users.service.get_connection") as mock_user_conn:
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn
        mock_user_conn.return_value = conn
        yield conn, cursor

def test_register_then_login(mock_db):
    """Full flow: register a user then log in with same credentials."""
    mock_conn, mock_cursor = mock_db

    # Step 1 — register
    # no existing user found
    mock_cursor.fetchone.side_effect = [
        None,                                           # register: user doesn't exist
        {"id": 1, "name": "bob", "is_admin": False,
         "created_at": "2024-01-01"},                  # register: return new user
        {"id": 1, "name": "bob",                       # login: fetch user from DB
         "password": "$hashed", "is_admin": False}
    ]

    with patch("src.users.service.pwd_context.hash", return_value="$hashed"), \
         patch("src.auth.service.pwd_context.verify", return_value=True):

        reg_response = client.post(
            "/api/auth/register",
            json={"name": "bob", "password": "secret"}
        )
        assert reg_response.status_code == 200
        assert reg_response.json()["message"] == "User registered successfully"

        # Step 2 — login with same user
        login_response = client.post(
            "/api/auth/login",
            json={"name": "bob", "password": "secret"}
        )
        assert login_response.status_code == 200
        assert "token" in login_response.json()

def test_login_with_wrong_password(mock_db):
    """Full flow: login fails with wrong password."""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = {
        "id": 1, "name": "alice",
        "password": "$hashed", "is_admin": False
    }

    with patch("src.auth.service.pwd_context.verify", return_value=False):
        response = client.post(
            "/api/auth/login",
            json={"name": "alice", "password": "wrongpassword"}
        )
    assert response.status_code == 401

def test_login_nonexistent_user(mock_db):
    """Full flow: login fails when user doesn't exist."""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None

    response = client.post(
        "/api/auth/login",
        json={"name": "ghost", "password": "password"}
    )
    assert response.status_code == 401