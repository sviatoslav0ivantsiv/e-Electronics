import pytest
from tests.integration.conftest import client


def test_get_all_users_as_admin(mock_db):
    """Full flow: admin fetches user list."""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [
        {"id": 1, "name": "admin", "is_admin": True},
        {"id": 2, "name": "user", "is_admin": False}
    ]

    response = client.get("/api/admin/users")   # require_admin overridden
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_toggle_admin_flow(mock_db):
    """Full flow: toggle admin status for a user."""
    mock_conn, mock_cursor = mock_db

    response = client.patch("/api/admin/users/2/toggle-admin")
    assert response.status_code == 200
    assert response.json()["message"] == "Admin status updated"

    # verify real SQL was built and executed
    mock_cursor.execute.assert_called_once_with(
        "UPDATE users SET is_admin = NOT is_admin WHERE id = %s", (2,)
    )