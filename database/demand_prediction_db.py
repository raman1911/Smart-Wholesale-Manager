from .connection_db import connect_db

def save_demand_prediction(company_id, product_id, forecast_date, predicted_quantity):
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO demand_prediction_history(company_id, product_id, forecast_date, predicted_quantity) VALUES(%s,%s,%s,%s)""",(company_id, product_id, forecast_date, predicted_quantity))

        conn.commit()
        return True

    except Exception as error:
        conn.rollback()
        print("Demand Prediction Save Error:", error)
        return False

    finally:
        cursor.close()
        conn.close()

def get_demand_predictions(company_id):
    conn = connect_db()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT dp.prediction_id, dp.product_id, p.product_name, dp.forecast_date, dp.predicted_quantity, dp.created_date
            FROM demand_prediction_history dp
            JOIN products p
            ON dp.product_id = p.product_id
            WHERE dp.company_id=%s
            ORDER BY dp.prediction_id DESC
            """, (company_id,))

        return cursor.fetchall() or []

    except Exception as error:
        print("Demand Prediction Fetch Error:", error)
        return []

    finally:
        cursor.close()
        conn.close()