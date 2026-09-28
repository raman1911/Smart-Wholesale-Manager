import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection_db import connect_db
conn = connect_db()
if conn:
    print("Database connection successful")
    conn.close()
else:
    print("Database connection failed")