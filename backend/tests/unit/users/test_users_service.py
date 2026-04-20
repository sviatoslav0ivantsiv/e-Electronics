import pytest
from unittest.mock import MagicMock, patch
from src.users.service import register, get_all, toggle_admin

@pytest.fixture
def mock_db():
    """Fixture to mock database connection and cursor."""
    with patch("src.users.service.get_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn, mock_cursor

class TestUsersService:

    def test_register_user_already_exists(self, mock_db):
        """Tests that register raises ValueError if the username is taken."""
        mock_conn, mock_cursor = mock_db
        # Simulate finding an existing user
        mock_cursor.fetchone.return_value = {"id": 1, "name": "alice"}
        
        with pytest.raises(ValueError, match="User already exists"):
            register("alice", "password123")
        
        # Ensure resources were cleaned up before raising
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_register_success(self, mock_db):
        """Tests successful user registration and password hashing."""
        mock_conn, mock_cursor = mock_db
        
        # 1. First fetchone (check existence) returns None
        # 2. Second fetchone (return new user) returns user data
        mock_cursor.fetchone.side_effect = [
            None, 
            {"id": 10, "name": "bob", "is_admin": False, "created_at": "2023-01-01"}
        ]
        mock_cursor.lastrowid = 10
        
        with patch("src.users.service.pwd_context.hash") as mock_hash:
            mock_hash.return_value = "hashed_secret"
            result = register("bob", "secret")
            
        assert result["message"] == "User registered successfully"
        assert result["user"]["id"] == 10
        assert mock_hash.called
        mock_conn.commit.assert_called_once()
        assert mock_cursor.close.call_count == 1

    def test_get_all_users(self, mock_db):
        """Tests retrieval of all users."""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "alice"},
            {"id": 2, "name": "bob"}
        ]
        
        users = get_all()
        
        assert len(users) == 2
        assert users[0]["name"] == "alice"
        mock_cursor.execute.assert_called_with("SELECT id, name, is_admin, created_at FROM users")
        mock_conn.close.assert_called_once()

    def test_toggle_admin_status(self, mock_db):
        """Tests toggling the is_admin boolean for a user."""
        mock_conn, mock_cursor = mock_db
        
        result = toggle_admin(5)
        
        assert result["message"] == "Admin status updated"
        mock_cursor.execute.assert_called_once_with(
            "UPDATE users SET is_admin = NOT is_admin WHERE id = %s", (5,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()