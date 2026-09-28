import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connect_timeout=5
        )

    except mysql.connector.Error as error:
        print(f"Database Connection Error: {error}")
        return None