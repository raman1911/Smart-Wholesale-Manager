import bcrypt
import mysql.connector
from .connection_db import connect_db
from .utils_db import _fetch_one

def get_company_details(company_id):
    query = """SELECT * FROM company WHERE company_id=%s"""
    return _fetch_one(query, (company_id,))

def hash_password(password):
    hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_bytes.decode()

def register_company(company_name, owner_name, business_type, gst_number, phone, email, address, city, state, pincode,  username, password):

    if _fetch_one("SELECT company_id FROM company WHERE company_name=%s", (company_name,)):
        return False, "Company name already exists"

    if _fetch_one("SELECT user_id FROM users WHERE username=%s", (username,)):
        return False, "Username already exists"

    if email:
        if _fetch_one("SELECT company_id FROM company WHERE email=%s", (email,)):
            return False, "Email already registered"

    if gst_number:
        if _fetch_one("SELECT company_id FROM company WHERE gst_number=%s", (gst_number,)):
            return False, "GST Number already registered"

    conn = connect_db()
    if conn is None:
        return False, "Database connection failed"

    cursor = conn.cursor()
    try:
        company_query = """INSERT INTO company(company_name, owner_name, business_type, gst_number, phone, email, address, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(company_query, (company_name, owner_name, business_type, gst_number if gst_number else None, phone, email, address, city, state, pincode))

        company_id = cursor.lastrowid

        user_query = """INSERT INTO users(company_id, username, password, role) VALUES (%s,%s,%s,%s)"""

        cursor.execute(user_query, (company_id, username, hash_password(password), "Admin"))

        conn.commit()
        return True, "Company registered successfully"

    except mysql.connector.Error as error:

        conn.rollback()
        print("Registration Error:", error)
        return False, "Registration failed"

    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = connect_db()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        query = """SELECT user_id, company_id, username, password, role FROM users WHERE username = %s"""

        cursor.execute( query, (username,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode(), user["password"].encode()):
                user.pop("password")
                return user

        return None

    except mysql.connector.Error as error:
        print("Login Error:", error)
        return None

    finally:
        cursor.close()
        conn.close()