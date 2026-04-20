import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.products.controller import router
from main import app
from src.auth.controller import require_admin



async def override_require_admin():
    return {"id": 1, "name": "admin", "is_admin": True}

app.dependency_overrides[require_admin] = override_require_admin
client = TestClient(app)

VALID_PRODUCT = {
    "category": "smartphone",
    "brand": "Samsung",
    "model": "Galaxy S24",
    "price": 999.0,
    "stock": 10
}


@pytest.fixture
def mock_service():
    with patch("src.products.controller.service") as mock:
        yield mock

class TestProductsController:

    def test_list_products_success(self, mock_service):
        """Tests that list_products returns data from the service."""
        mock_service.get_products.return_value = {"products": [{"id": 1, "name": "Test"}], "total": 1}
        
        response = client.get("/api/products")
        
        assert response.status_code == 200
        assert response.json()["total"] == 1
        mock_service.get_products.assert_called_once()

    def test_get_product_by_id_success(self, mock_service):
        mock_service.get_by_id.return_value = {"id": 1, **VALID_PRODUCT}
        response = client.get("/api/products/1")
        assert response.status_code == 200

    def test_get_product_by_id_not_found(self, mock_service):
        mock_service.get_by_id.return_value = None
        response = client.get("/api/products/999")
        assert response.status_code == 404

    def test_get_filters_success(self, mock_service):
        """Tests retrieval of filter options."""
        mock_service.get_filter_options.return_value = {"brand": ["Apple"]}
        
        response = client.get("/api/products/filters?category=laptop")
        
        assert response.status_code == 200
        assert "Apple" in response.json()["brand"]
        mock_service.get_filter_options.assert_called_once_with("laptop")

    def test_get_filters_error(self, mock_service):
        """Tests 500 error when get_filters fails."""
        mock_service.get_filter_options.side_effect = Exception("Service unavailable")
        
        response = client.get("/api/products/filters")
        
        assert response.status_code == 500
        assert "Service unavailable" in response.json()["detail"]

    def test_create_product_success(self, mock_service):
        """Tests successful product creation."""
                
        response = client.post("/api/products", json=VALID_PRODUCT)

        print(response.json())
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product created"
        mock_service.save.assert_called_once()

    def test_create_product_validation_error(self, mock_service):
        """Tests 400 error when service.save raises an exception."""
        mock_service.save.side_effect = Exception("Missing required field")
        
        response = client.post("/api/products", json=VALID_PRODUCT)
        
        assert response.status_code == 400
        assert "Missing required field" in response.json()["detail"]

    def test_create_product_missing_required_fields(self, mock_service):
        """Tests that FastAPI rejects incomplete body with 422."""
        response = client.post("/api/products", json={"price": 999})
        assert response.status_code == 422
        mock_service.save.assert_not_called() 

    def test_update_product_full(self, mock_service):
        """Tests the PUT endpoint for full updates."""
                
        response = client.put("/api/products/1", json=VALID_PRODUCT)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product updated"
        # Verify that exclude_none=True was passed to model_dump
        call_args = mock_service.update.call_args[0]
        assert None not in call_args[1].values()

    def test_patch_product_partial(self, mock_service):
        """Tests the PATCH endpoint for partial updates."""
        
        partial_data = {"price": 500.0}

        response = client.patch("/api/products/1", json=partial_data)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product partially updated"
        mock_service.update.assert_called_once()

    def test_delete_product_success(self, mock_service):
        """Tests product deletion."""
        mock_service.delete.return_value = {"message": "Product deleted"}
        
        response = client.delete("/api/products/10")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted"
        mock_service.delete.assert_called_once_with(10)

    def test_delete_product_failure(self, mock_service):
        """Tests 400 error when deletion fails."""
        mock_service.delete.side_effect = Exception("Product not found")
        response = client.delete("/api/products/999")
        assert response.status_code == 400
        assert "Product not found" in response.json()["detail"]