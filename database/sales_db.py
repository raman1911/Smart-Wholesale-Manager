from .connection_db import connect_db
import pandas as pd

def get_sales_orders(company_id, search=None):
    query = """SELECT s.sale_id, s.product_id, s.bill_number, s.sale_date, s.quantity, s.selling_price, s.total_amount, s.customer_name, s.customer_phone, pr.product_name, s.created_date
    FROM sales s
    LEFT JOIN products pr
    ON s.product_id = pr.product_id
    WHERE s.company_id = %s"""

    params = [company_id]

    if search:
        query += """ AND (s.bill_number LIKE %s OR s.customer_name LIKE %s OR s.customer_phone LIKE %s OR pr.product_name LIKE %s)"""

        like_search = f"%{search}%"

        params.extend([like_search, like_search, like_search, like_search])

    query += """ ORDER BY s.sale_id DESC"""

    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        return cursor.fetchall() or []

    except Exception as error:
        print("Sales Fetch Error:", error)
        return []

    finally:
        cursor.close()
        conn.close()

def add_sales_order(company_id, customer_name, customer_phone, sale_date, items):
    if not items:
        return None

    conn = connect_db()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        for item in items:
            cursor.execute(
            """SELECT product_id, product_name, stock_quantity FROM products
                WHERE product_id=%s AND company_id=%s FOR UPDATE""",
                (item["product_id"], company_id))

            product = cursor.fetchone()

            if product is None:
                conn.rollback()

                return {"status": "PRODUCT_NOT_FOUND", "product_name": item.get("product_name", "")}

            requested_quantity = int(item["quantity"])
            available_quantity = int(product["stock_quantity"])

            if requested_quantity > available_quantity:
                conn.rollback()

                return {"status": "INSUFFICIENT_STOCK", "product_name": product["product_name"], "available": available_quantity, "requested": requested_quantity}
            
        first_sale_id = None
        sale_ids = []

        for item in items:
            product_id = int(item["product_id"])
            quantity = int(item["quantity"])
            selling_price = float(item["selling_price"])
            total_amount = round(quantity * selling_price, 2)

            cursor.execute("""INSERT INTO sales(company_id, product_id, customer_name, customer_phone, quantity, selling_price, total_amount, sale_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", (company_id, product_id, customer_name, customer_phone, quantity, selling_price, total_amount, sale_date))

            sale_id = cursor.lastrowid

            sale_ids.append(sale_id)

            if first_sale_id is None:
                first_sale_id = sale_id

            cursor.execute("""UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s AND company_id=%s""", (quantity, product_id, company_id))

        bill_number = f"BILL.S{first_sale_id:04d}"
        placeholders = ",".join(["%s"] * len(sale_ids))

        cursor.execute(f""" UPDATE sales SET bill_number=%s WHERE company_id=%s AND sale_id IN ({placeholders})""", (bill_number, company_id, *sale_ids))

        conn.commit()

        grand_total = sum(float(item["quantity"]) * float(item["selling_price"]) for item in items)

        return {"status": "SUCCESS", "bill_number": bill_number, "sale_id": first_sale_id, "grand_total": round(grand_total, 2)}

    except Exception as error:
        conn.rollback()
        print("Sales Order Insert Error:", error)

        return {"status": "ERROR", "message": str(error)}

    finally:
        cursor.close()
        conn.close()

def get_sales_data_for_ml(company_id):
    query = """SELECT sales.sale_id, sales.product_id, sales.quantity, sales.selling_price, sales.total_amount, sales.sale_date, products.product_name FROM sales
    JOIN products
    ON sales.product_id = products.product_id
    WHERE sales.company_id = %s
    ORDER BY sales.sale_date"""

    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, (company_id,))
        rows = cursor.fetchall()
        return pd.DataFrame(rows)

    except Exception as error:
        print("ML Sales Data Fetch Error:", error)
        return []

    finally:
        cursor.close()
        conn.close()