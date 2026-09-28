import mysql.connector
from .connection_db import connect_db

def _fetch_all(query, params=()):
    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchall() or []
    
    except mysql.connector.Error as error:
        print("Database Fetch Error:", error)
        return []
    
    finally:
        cursor.close()
        conn.close()

def _fetch_one(query, params=()):
    conn = connect_db()

    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    
    except mysql.connector.Error as error:
        print("Database Fetch Error:", error)
        return None
    
    finally:
        cursor.close()
        conn.close()

def _execute_commit(query, params=(), fetch_lastrow=False):
    conn = connect_db()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid if fetch_lastrow else True
    
    except mysql.connector.Error as error:
        conn.rollback()
        print("Database Commit Error:", error)
        return None
    
    finally:
        cursor.close()
        conn.close()
