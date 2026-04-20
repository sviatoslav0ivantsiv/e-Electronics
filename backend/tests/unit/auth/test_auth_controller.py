import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import MagicMock, patch
from jose import JWTError
from src.auth.controller import router, require_admin


app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_auth_service():
    with patch("src.auth.service.login") as mock:
        yield mock

@pytest.fixture
def mock_jwt():
    with patch("src.auth.controller.jwt") as mock:
        yield mock

class TestAuthController:
    
    def test_login_success(self, mock_auth_service):
        """Tests that a valid login returns a 200 and a token."""
        mock_auth_service.return_value = "mocked_jwt_token"
        
        response = client.post(
            "/api/auth/login",
            json={"name": "admin", "password": "password123"}
        )
        
        assert response.status_code == 200
        assert response.json()["token"] == "mocked_jwt_token"
        assert response.json()["message"] == "Login successful"

    def test_login_invalid_credentials(self, mock_auth_service):
        """Tests that login returns 401 when the service returns no token."""
        mock_auth_service.return_value = None
        
        response = client.post(
            "/api/auth/login",
            json={"name": "user", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_internal_error(self, mock_auth_service):
        """Tests that 500 is returned if the service raises an exception."""
        mock_auth_service.side_effect = Exception("Database connection lost")
        
        response = client.post(
            "/api/auth/login",
            json={"name": "user", "password": "password"}
        )
        
        assert response.status_code == 500
        assert "Database connection lost" in response.json()["detail"]

class TestRequireAdminDependency:
    
    def test_require_admin_success(self, mock_jwt):
        """Tests dependency returns payload when user is admin."""
        mock_jwt.decode.return_value = {"id": 1, "is_admin": True}
        credentials = MagicMock()
        credentials.credentials = "valid_admin_token"
        
        result = require_admin(credentials)
        assert result["is_admin"] is True

    def test_require_admin_forbidden(self, mock_jwt):
        """Tests dependency raises 403 when user is not admin."""
        mock_jwt.decode.return_value = {"id": 2, "is_admin": False}
        credentials = MagicMock()
        credentials.credentials = "valid_user_token"
        
        with pytest.raises(Exception) as excinfo:
            require_admin(credentials)
        assert excinfo.value.status_code == 403
        assert excinfo.value.detail == "Admins only"

    def test_require_admin_invalid_token(self, mock_jwt):
        """Tests dependency raises 401 on JWT decoding errors."""
        mock_jwt.decode.side_effect = JWTError("Invalid signature")
        credentials = MagicMock()
        
        with pytest.raises(Exception) as excinfo:
            require_admin(credentials)
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid token"