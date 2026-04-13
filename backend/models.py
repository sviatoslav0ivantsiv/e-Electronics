from db import get_connection
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(Path(__file__).resolve().parent / ".env")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")

# ======================== products ==========================

class Product:
    def __init__(self, category, brand, model, price, stock=0, **kwargs):
        self.category = category
        self.brand = brand
        self.model = model
        self.price = price
        self.stock = stock
        self.specs = kwargs  # other fields like cpu, ram, etc. will be stored here

    @staticmethod
    def get_products(category = None, brand = None, min_price = None, max_price = None, model = None,
                     min_display_size = None, max_display_size = None, min_battery_capacity = None, max_battery_capacity = None,
                     camera = None, cpu = None, gpu = None, min_screen_size = None, max_screen_size = None, min_weight = None, max_weight = None,
                     screen_type = None, min_battery_life = None, max_battery_life = None, water_resistance = None,
                     ram = None, storage = None,
                     sort = "desc",
                     page = 1, limit = 10 ):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sorting = ["asc", "desc"]
        limit = min(limit, 100)
        offset = (page - 1) * limit


        sql = ""
        params = []

        if category:
            sql += " AND category = %s"
            params.append(category)
        if brand:
            if isinstance(brand, list):
                placeholders = ', '.join(['%s'] * len(brand))
                sql += f" AND brand IN ({placeholders})"
                params.extend(brand)
            else:
                sql += " AND brand = %s"
                params.append(brand)
        if min_price:
            sql += " AND price >= %s"
            params.append(min_price)
        if max_price:
            sql += " AND price <= %s"
            params.append(max_price)
        if model and model.strip():
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
            if isinstance(camera, list):
                placeholders = ', '.join(['%s'] * len(camera))
                sql += f" AND camera_mp IN ({placeholders})"
                params.extend(camera)
            else:
                sql += " AND camera_mp = %s"
                params.append(camera)
        if cpu:
            if isinstance(cpu, list):
                placeholders = ', '.join(['%s'] * len(cpu))
                sql += f" AND cpu IN ({placeholders})"
                params.extend(cpu)
            else:
                sql += " AND cpu = %s"
                params.append(cpu)
        if gpu:
            if isinstance(gpu, list):
                placeholders = ', '.join(['%s'] * len(gpu))
                sql += f" AND gpu IN ({placeholders})"
                params.extend(gpu)
            else:
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
            if isinstance(screen_type, list):
                placeholders = ', '.join(['%s'] * len(screen_type))
                sql += f" AND screen_type IN ({placeholders})"
                params.extend(screen_type)
            else:
                sql += " AND screen_type = %s"
                params.append(screen_type)
        if min_battery_life:
            sql += " AND battery_life >= %s"
            params.append(min_battery_life)
        if max_battery_life:
            sql += " AND battery_life <= %s"
            params.append(max_battery_life)
        if water_resistance:
            if isinstance(water_resistance, list):
                placeholders = ', '.join(['%s'] * len(water_resistance))
                sql += f" AND water_resistance IN ({placeholders})"
                params.extend(water_resistance)
            else:
                sql += " AND water_resistance = %s"
                params.append(water_resistance)
        if ram:
            if isinstance(ram, list):
                placeholders = ', '.join(['%s'] * len(ram))
                sql += f" AND ram IN ({placeholders})"
                params.extend(ram)
            else:
                sql += " AND ram = %s"
                params.append(ram)
        if storage:
            if isinstance(storage, list):
                placeholders = ', '.join(['%s'] * len(storage))
                sql += f" AND storage IN ({placeholders})"
                params.extend(storage)
            else:
                sql += " AND storage = %s"
                params.append(storage)
        if sort in sorting:
            direction = sort.upper()
        else:
            direction = "DESC"

        select_sql ="SELECT * FROM products WHERE 1=1" + sql + f" ORDER BY price {direction}" + " LIMIT %s OFFSET %s"
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

    @staticmethod
    def all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def save(data: dict):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO products (category, brand, model, price, stock)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data["category"],
            data["brand"],
            data["model"],
            data["price"],
            data.get("stock", 0)
        ))
        conn.commit()
        cursor.close()
        conn.close()

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


    # ==========filter options================
    
    @staticmethod
    def get_filter_options(category=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        where = "WHERE category = %s" if category else ""
        params = [category] if category else []

        fields = ["brand", "ram", "storage"]

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

    


# ======================== users ==========================



def create_token(user):
    return jwt.encode({"id": user["id"], "name": user["name"], "is_admin": user["is_admin"]}, SECRET_KEY, algorithm="HS256")

class UserRegister(BaseModel):
    name: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class User:
    @staticmethod
    def register(user: UserRegister):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE name = %s", (user.name,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {"message": "User already exists"}

        hashed = pwd_context.hash(user.password)

        cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (user.name, hashed))
        conn.commit()

        new_id = cursor.lastrowid
        cursor.execute("SELECT id, name, is_admin, created_at FROM users WHERE id = %s", (new_id,))
        new_user = cursor.fetchone()

        cursor.close()
        conn.close()
        return {
            "message": "User registered successfully",
            "user": new_user
        }

    @staticmethod
    def login(name: str, password: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()

        if not user or not pwd_context.verify(password, user["password"]):
            cursor.close()
            conn.close()
            return {"message": "Invalid credentials"}
        
        token = create_token(user)
        user["token"] = token

        return {
            "message": "Login successful",
            "token": token
        }
    
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, is_admin, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    @staticmethod
    def toggle_admin(user_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_admin = NOT is_admin WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Admin status updated"}