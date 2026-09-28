from .connection_db import connect_db

def purchase_exists(company_id, bill_number):
    query = """SELECT purchase_id FROM purchases WHERE company_id=%s AND bill_number=%s"""

    conn = connect_db()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, (company_id, bill_number))
        return cursor.fetchone()

    except Exception as error:
        print("Purchase Check Error:", error)
        return None

    finally:
        cursor.close()
        conn.close()

def get_purchase_orders(company_id, search=None):
    query = """SELECT p.purchase_id, p.bill_number, p.purchase_date, p.quantity, p.purchase_price, p.total_amount, d.dealer_name, pr.product_name, p.created_date FROM purchases p
    LEFT JOIN dealers d
    ON p.dealer_id = d.dealer_id
    LEFT JOIN products pr
    ON p.product_id = pr.product_id
    WHERE p.company_id=%s"""

    params = [company_id]

    if search:
        query += """ AND (p.bill_number LIKE %s OR d.dealer_name LIKE %s OR pr.product_name LIKE %s)"""
        like_search = f"%{search}%"

        params.extend([like_search, like_search, like_search])

    query += """ ORDER BY p.purchase_id DESC"""

    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        return cursor.fetchall() or []

    except Exception as error:
        print("Purchase Fetch Error:", error)
        return []

    finally:
        cursor.close()
        conn.close()

def add_purchase(company_id, dealer_id, product_id, bill_number, quantity, purchase_price, purchase_date):
    conn = connect_db()
    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        if purchase_exists(company_id, bill_number):
            return False

        cursor.execute("""SELECT product_id FROM products WHERE product_id=%s AND company_id=%s""", (product_id, company_id))

        if cursor.fetchone() is None:
            return None

        cursor.execute("""SELECT dealer_id FROM dealers WHERE dealer_id=%s AND company_id=%s""", (dealer_id, company_id))

        if cursor.fetchone() is None:
            return None

        total_amount = quantity * purchase_price

        cursor.execute("""INSERT INTO purchases(company_id, dealer_id, product_id, bill_number, quantity, purchase_price, total_amount, purchase_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", (company_id, dealer_id, product_id, bill_number, quantity, purchase_price, total_amount, purchase_date))

        purchase_id = cursor.lastrowid

        cursor.execute("""UPDATE products
            SET stock_quantity = stock_quantity + %s, purchase_price = %s
            WHERE product_id=%s AND company_id=%s""",
            (quantity, purchase_price, product_id, company_id))

        conn.commit()
        return purchase_id

    except Exception as error:
        conn.rollback()
        print("Purchase Insert Error:", error)
        return None

    finally:
        cursor.close()
        conn.close()