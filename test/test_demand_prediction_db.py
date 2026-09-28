import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.demand_prediction_db import get_demand_predictions
company_id = 1
predictions = get_demand_predictions(company_id)
print("Total Demand Predictions Found:", len(predictions))
print(predictions)