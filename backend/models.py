
from db import get_connection

class Product:
    def __init__(self, category, brand, model, price, stock=0, **kwargs):
        self.category = category
        self.brand = brand
        self.model = model
        self.price = price
        self.stock = stock
        self.specs = kwargs  # other fields like cpu, ram, etc. will be stored here
    @staticmethod
    def all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO products (category, brand, model, price, stock)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (self.category, self.brand, self.model, self.price, self.stock))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def paginate(page=1, limit=10):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = min(limit, 100)
        offset = (page - 1) * limit

        cursor.execute("SELECT * FROM products ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        products = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()

        return {
            "products": products,
            "total": total
        }

    @staticmethod
    def by_category(category, page=1, limit=10):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = min(limit, 100)
        offset = (page - 1) * limit

        cursor.execute("SELECT * FROM products WHERE category = %s ORDER BY id LIMIT %s OFFSET %s", (category, limit, offset))
        products = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) as total FROM products WHERE category = %s", (category,))
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()

        return {
            "products": products,
            "total": total

        }

    @staticmethod
    def update(product_id, data: dict):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE products
        SET category=%s, brand=%s, model=%s, price=%s, stock=%s
        WHERE id=%s
        """

        cursor.execute(sql, (
            data["category"],
            data["brand"],
            data["model"],
            data["price"],
            data.get("stock", 0),
            product_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Product updated"}

    @staticmethod
    def patch(product_id, data: dict):
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key}=%s")
            values.append(value)

        values.append(product_id)

        sql = f"""
        UPDATE products
        SET {', '.join(fields)}
        WHERE id=%s
        """

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Product partially updated"}

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Product deleted"}