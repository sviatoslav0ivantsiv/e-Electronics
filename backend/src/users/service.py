from passlib.context import CryptContext
from src.users.model import UserRegister
from src.database.core import get_connection
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE name = %s", (user.name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        logging.error(f"User {user.name} already exists")
        return  {"message": "User already exists"}

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

def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, is_admin, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def toggle_admin(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_admin = NOT is_admin WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Admin status updated"}