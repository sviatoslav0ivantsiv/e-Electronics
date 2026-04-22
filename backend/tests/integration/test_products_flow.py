import pytest
from tests.integration.conftest import client

VALID_PRODUCT = {
    "category": "smartphone",
    "brand": "Samsung",
    "model": "Galaxy S24",
    "price": 999.0,
    "stock": 10
}

def test_create_then_fetch_product(mock_db):
    """Full flow: create a product then retrieve it."""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [
        {"id": 1, "brand": "Samsung", "model": "S24", "price": 999}
    ]
    mock_cursor.fetchone.return_value = {"total": 1}
    
    create_response = client.post("/api/products", json=VALID_PRODUCT)
    assert create_response.status_code == 200

    list_response = client.get("/api/products")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1