import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sales_prediction_db import get_sales_predictions
company_id = 1
predictions = get_sales_predictions(company_id)
print("Total Sales Predictions Found:", len(predictions))
print(predictions)