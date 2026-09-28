from .connection_db import connect_db

def save_sales_prediction(company_id, product_id, prediction_date, quantity, selling_price, predicted_sales):
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO sales_prediction_history(company_id, product_id, prediction_date, quantity, selling_price, predicted_sales) VALUES(%s,%s,%s,%s,%s,%s)""", (company_id, product_id, prediction_date, quantity, selling_price, predicted_sales))

        conn.commit()
        return True

    except Exception as error:
        conn.rollback()
        print("Sales Prediction Save Error:", error)
        return False

    finally:
        cursor.close()
        conn.close()

def get_sales_predictions(company_id):
    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""SELECT sp.prediction_id, sp.product_id, p.product_name, sp.prediction_date, sp.quantity, sp.selling_price, sp.predicted_sales, sp.created_date FROM sales_prediction_history sp
            JOIN products p ON sp.product_id = p.product_id
            WHERE sp.company_id=%s
            ORDER BY sp.prediction_id DESC""", 
            (company_id,))

        return cursor.fetchall() or []

    except Exception as error:
        print("Sales Prediction Fetch Error:", error)
        return []

    finally:
        cursor.close()
        conn.close()