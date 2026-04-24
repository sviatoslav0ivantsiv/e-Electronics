import pytest
from unittest.mock import MagicMock, patch
from src.products.service import get_products, save, update, delete, get_filter_options

@pytest.fixture
def mock_db():
    """Fixture to mock database connection and cursor."""
    with patch("src.products.service.get_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn, mock_cursor

class TestProductsService:

    def test_get_products_with_basic_filters(self, mock_db):
        """Tests get_products with category and price range filters."""
        mock_conn, mock_cursor = mock_db
        
        # Mock return values for product list and total count
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "Phone"}]
        mock_cursor.fetchone.return_value = {"total": 1}
        
        filters = {"category": "smartphone", "min_price": 500}
        result = get_products(filters)
        
        assert len(result["products"]) == 1
        assert result["total"] == 1
        
        # Verify SQL construction (check if placeholders were added)
        calls = mock_cursor.execute.call_args_list
        select_sql = calls[0][0][0]
        params = calls[0][0][1]
        
        assert "category = %s" in select_sql
        assert "price >= %s" in select_sql
        assert "smartphone" in params
        assert 500 in params

    def test_get_products_with_list_filters(self, mock_db):
        """Tests the IN clause generation for list-based filters like brand."""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = {"total": 0}
        
        filters = {"brand": ["Apple", "Samsung"]}
        get_products(filters)
        
        select_sql = mock_cursor.execute.call_args_list[0][0][0]
        params = mock_cursor.execute.call_args_list[0][0][1]
        
        assert "brand IN (%s, %s)" in select_sql
        assert "Apple" in params
        assert "Samsung" in params

    def test_save_product(self, mock_db):
        """Tests that save cleans None values and executes INSERT."""
        mock_conn, mock_cursor = mock_db
        
        data = {"name": "Laptop", "price": 1000, "description": None}
        save(data)
        
        sql = mock_cursor.execute.call_args[0][0]
        params = mock_cursor.execute.call_args[0][1]
        
        assert "INSERT INTO products" in sql
        assert "description" not in sql  # None values should be cleaned
        assert "Laptop" in params
        mock_conn.commit.assert_called_once()

    def test_update_product(self, mock_db):
        """Tests product update logic."""
        mock_conn, mock_cursor = mock_db
        
        update(123, {"price": 899})
        
        sql = mock_cursor.execute.call_args[0][0]
        params = mock_cursor.execute.call_args[0][1]
        
        assert "UPDATE products SET price=%s WHERE id=%s" in sql
        assert params == [899, 123]
        mock_conn.commit.assert_called_once()

    def test_delete_product(self, mock_db):
        """Tests product deletion."""
        mock_conn, mock_cursor = mock_db
        
        delete(5)
        
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM products WHERE id=%s", (5,)
        )
        mock_conn.commit.assert_called_once()

    def test_get_filter_options_for_laptop(self, mock_db):
        """Tests that filter options include category-specific fields."""
        mock_conn, mock_cursor = mock_db
        # Return empty list for each DISTINCT query
        mock_cursor.fetchall.return_value = []
        
        result = get_filter_options(category="laptop")
        
        # Verify that specific laptop fields were queried
        assert "cpu" in result
        assert "gpu" in result
        assert "brand" in result
        
        # Ensure query used the category filter
        last_sql = mock_cursor.execute.call_args[0][0]
        assert "WHERE category = %s" in last_sql

    def test_get_filter_options_no_category(self, mock_db):
        """Tests filter options without category restriction."""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchall.return_value = []
        
        result = get_filter_options()
        assert "cpu" not in result # Field specific to laptops
        assert "brand" in result