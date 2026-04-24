import mysql.connector
import os
import tempfile
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

ssl_ca_content = os.getenv("DB_SSL_CA")
ssl_args = {}
if ssl_ca_content:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    tmp.write(ssl_ca_content.encode())
    tmp.close()
    ssl_args = {"ssl_ca": tmp.name}

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 8889)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "electronics-1"),
        raise_on_warnings=True
    )