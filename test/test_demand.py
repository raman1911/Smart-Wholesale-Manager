import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.demand_prediction import predict_demand
company_id = 1
product_id = 1
prediction = predict_demand( company_id, product_id, 30, 9, 2026)
print("Predicted Demand:", prediction)