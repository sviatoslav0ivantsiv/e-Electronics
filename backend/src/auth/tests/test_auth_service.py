import pytest
from unittest.mock import MagicMock, patch
from jose import jwt
from src.auth.service import create_token, login, SECRET_KEY, ALGORITHM

def test_create_token_contains_correct_payload():
    """Tests that the generated JWT contains the expected user data."""
    user = {"id": 1, "name": "alice", "is_admin": True}
   
    test_key = SECRET_KEY or "test_secret"
    test_algo = ALGORITHM or "HS256"
    
    with patch("src.auth.service.SECRET_KEY", test_key), \
         patch("src.auth.service.ALGORITHM", test_algo):
        token = create_token(user)
        payload = jwt.decode(token, test_key, algorithms=[test_algo])
        
    assert payload["id"] == user["id"]
    assert payload["name"] == user["name"]
    assert payload["is_admin"] == user["is_admin"]

@patch("src.auth.service.get_connection")
@patch("src.auth.service.pwd_context.verify")
def test_login_success(mock_verify, mock_get_conn):
    """Tests successful login when user exists and password matches."""
    # Mock DB Connection and Cursor
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    mock_get_conn.return_value = mock_conn
    
    # Mock DB response
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "name": "alice",
        "password": "hashed_password",
        "is_admin": False
    }
    mock_verify.return_value = True
    
    with patch("src.auth.service.SECRET_KEY", "secret"):
        token = login("alice", "plain_password")
    
    assert token is not None
    mock_cursor.execute.assert_called_once()
    mock_verify.assert_called_once_with("plain_password", "hashed_password")
    mock_conn.close.assert_called_once()

@patch("src.auth.service.get_connection")
def test_login_user_not_found(mock_get_conn):
    """Tests that login returns None when the user does not exist in the DB."""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    mock_get_conn.return_value = mock_conn
    
    mock_cursor.fetchone.return_value = None
    
    token = login("nonexistent", "password")
    
    assert token is None
    mock_conn.close.assert_called_once()

@patch("src.auth.service.get_connection")
@patch("src.auth.service.pwd_context.verify")
def test_login_invalid_password(mock_verify, mock_get_conn):
    """Tests that login returns None when the password verification fails."""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    mock_get_conn.return_value = mock_conn
    
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "name": "alice",
        "password": "hashed_password",
        "is_admin": False
    }
    mock_verify.return_value = False
    
    token = login("alice", "wrong_password")
    
    assert token is None
    mock_conn.close.assert_called_once()

@patch("src.auth.service.get_connection")
def test_login_db_connection_failure(mock_get_conn):
    """Tests that login handles DB connection errors gracefully."""
    mock_get_conn.side_effect = Exception("DB unreachable")
        
    token = login("alice", "password")
        
    assert token is None
    mock_get_conn.assert_called_once()


def test_create_token_raises_without_secret_key():
    """Tests that create_token fails loudly if SECRET_KEY is missing."""
    user = {"id": 1, "name": "alice", "is_admin": False}
    
    with patch("src.auth.service.SECRET_KEY", None):
        with pytest.raises(Exception):
            create_token(user)