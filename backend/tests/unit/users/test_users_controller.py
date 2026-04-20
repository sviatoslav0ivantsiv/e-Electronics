import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import MagicMock, patch
from src.users.controller import router
from src.auth.controller import require_admin

# Setup test application
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Mock the require_admin dependency for admin-only routes
async def override_require_admin():
    return {"id": 1, "name": "admin", "is_admin": True}

app.dependency_overrides[require_admin] = override_require_admin

@pytest.fixture
def mock_user_service():
    with patch("src.users.controller.service") as mock:
        yield mock

class TestUsersController:

    def test_register_user_success(self, mock_user_service):
        """Tests successful user registration."""
        mock_user_service.register.return_value = {
            "message": "User registered successfully",
            "user": {"id": 1, "name": "testuser", "is_admin": False}
        }

        response = client.post(
            "/api/auth/register",
            json={"name": "testuser", "password": "password123"}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "User registered successfully"
        mock_user_service.register.assert_called_once_with("testuser", "password123")

    def test_register_user_already_exists(self, mock_user_service):
        """Tests registration failure when user already exists (409)."""
        mock_user_service.register.side_effect = ValueError("User already exists")

        response = client.post(
            "/api/auth/register",
            json={"name": "existinguser", "password": "password123"}
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "User already exists"

    def test_get_users_success(self, mock_user_service):
        """Tests that admins can retrieve the user list."""
        mock_user_service.get_all.return_value = [
            {"id": 1, "name": "admin", "is_admin": True},
            {"id": 2, "name": "user", "is_admin": False}
        ]

        response = client.get("/api/admin/users")

        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_user_service.get_all.assert_called_once()

    def test_get_users_internal_error(self, mock_user_service):
        """Tests 500 error handling in get_users."""
        mock_user_service.get_all.side_effect = Exception("DB Error")

        response = client.get("/api/admin/users")

        assert response.status_code == 500
        assert response.json()["detail"] == "DB Error"

    def test_toggle_admin_success(self, mock_user_service):
        """Tests successful admin status toggle."""
        mock_user_service.toggle_admin.return_value = {"message": "Admin status updated"}

        response = client.patch("/api/admin/users/2/toggle-admin")

        assert response.status_code == 200
        assert response.json()["message"] == "Admin status updated"
        mock_user_service.toggle_admin.assert_called_once_with(2)

    def test_toggle_admin_failure(self, mock_user_service):
        """Tests 400 error handling in toggle_admin."""
        mock_user_service.toggle_admin.side_effect = Exception("User not found")

        response = client.patch("/api/admin/users/99/toggle-admin")

        assert response.status_code == 400
        assert response.json()["detail"] == "User not found"