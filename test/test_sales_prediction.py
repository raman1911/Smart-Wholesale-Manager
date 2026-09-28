import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.sales_prediction import predict_sales
company_id = 1
product_id = 1
prediction = predict_sales( company_id=company_id, product_id=product_id, day=27, month=9, year=2026, selling_price=100)
print("Predicted Sales Revenue:", prediction)

from ml_models.sales_prediction import evaluate_sales_model
error = evaluate_sales_model(company_id, product_id)
print("Average prediction error (₹):", error)