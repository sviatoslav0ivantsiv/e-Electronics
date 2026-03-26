
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
    def get_products(category = None, brand = None, min_price = None, max_price = None, model = None,
                     min_display_size = None, max_display_size = None, min_battery_capacity = None, max_battery_capacity = None,
                     camera = None, cpu = None, gpu = None, min_screen_size = None, max_screen_size = None, min_weight = None, max_weight = None,
                     screen_type = None, min_battery_life = None, max_battery_life = None, water_resistance = None,
                     ram=None, storage=None,
                     page = 1, limit = 10 ):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = min(limit, 100)
        offset = (page - 1) * limit

        sql = ""
        params = []

        if category:
            sql += " AND category = %s"
            params.append(category)
        if brand:
            sql += " AND brand = %s"
            params.append(brand)
        if min_price:
            sql += " AND price >= %s"
            params.append(min_price)
        if max_price:
            sql += " AND price <= %s"
            params.append(max_price)
        if model:
            sql += " AND model LIKE %s"
            params.append(f"%{model}%")
        if min_display_size:
            sql += " AND display_size >= %s"
            params.append(min_display_size)
        if max_display_size:
            sql += " AND display_size <= %s"
            params.append(max_display_size)
        if min_battery_capacity:
            sql += " AND battery_capacity >= %s"
            params.append(min_battery_capacity)
        if max_battery_capacity:
            sql += " AND battery_capacity <= %s"
            params.append(max_battery_capacity)
        if camera:
            sql += " AND camera_mp = %s"
            params.append(camera)
        if cpu:
            sql += " AND cpu = %s"
            params.append(cpu)
        if gpu:
            sql += " AND gpu = %s"
            params.append(gpu)
        if min_screen_size:
            sql += " AND screen_size >= %s"
            params.append(min_screen_size)
        if max_screen_size:
            sql += " AND screen_size <= %s"
            params.append(max_screen_size)
        if min_weight:
            sql += " AND weight >= %s"
            params.append(min_weight)
        if max_weight:
            sql += " AND weight <= %s"
            params.append(max_weight)
        if screen_type:
            sql += " AND screen_type = %s"
            params.append(screen_type)
        if min_battery_life:
            sql += " AND battery_life >= %s"
            params.append(min_battery_life)
        if max_battery_life:
            sql += " AND battery_life <= %s"
            params.append(max_battery_life)
        if water_resistance:
            sql += " AND water_resistance = %s"
            params.append(water_resistance)
        if ram:
            sql += " AND ram = %s"
            params.append(ram)
        if storage:
            sql += " AND storage = %s"
            params.append(storage)

        select_sql ="SELECT * FROM products WHERE 1=1" + sql + " LIMIT %s OFFSET %s"
        cursor.execute(select_sql, params + [limit, offset])
        products = cursor.fetchall()

        count_sql = "SELECT COUNT(*) as total FROM products WHERE 1=1" + sql
        cursor.execute(count_sql, params)
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()

        return {
            "products": products,
            "total": total
        }

    # @staticmethod
    # def get_filter_options(category=None):
    #     conn = get_connection()
    #     cursor = conn.cursor(dictionary=True)
    #
    #     where = "WHERE category = %s" if category else ""
    #     params = [category] if category else []
    #
    #     result = {}
    #     for col in ["brand", "ram", "storage", "cpu", "gpu", "screen_type", "water_resistance"]:
    #         cursor.execute(f"SELECT DISTINCT {col} FROM products {where} ORDER BY {col}", params)
    #         result[col] = [row[col] for row in cursor.fetchall() if row[col]]
    #
    #     cursor.close()
    #     conn.close()
    #     return result

    @staticmethod
    def get_filter_options(category=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        where = "WHERE category = %s" if category else ""
        params = [category] if category else []

        # always show these
        fields = ["brand", "ram", "storage"]

        # category-specific
        if category == "laptop":
            fields += ["cpu", "gpu"]
        elif category == "smartphone":
            fields += ["camera_mp"]
        elif category == "smartwatch":
            fields += ["screen_type", "water_resistance"]

        result = {}
        for col in fields:
            cursor.execute(f"SELECT DISTINCT {col} FROM products {where} ORDER BY {col}", params)
            result[col] = [row[col] for row in cursor.fetchall() if row[col] is not None]

        cursor.close()
        conn.close()
        return result






