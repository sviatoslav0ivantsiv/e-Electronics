from src.database.core import get_connection
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def create_token(user: dict):
    payload = {
        "id": user["id"],
        "name": user["name"],
        "is_admin": user["is_admin"]
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def login(name: str, password: str):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()
        if not user:
            return None
        if not pwd_context.verify(password, user["password"]):
            return None
        token = create_token(user)
        return token
    except Exception as e:
        print("Error during login:", e)
        raise
    finally:
        if conn:
            conn.close()
