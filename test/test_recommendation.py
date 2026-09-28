import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.recommendation import generate_business_recommendations
company_id = 1
recommendations = generate_business_recommendations(company_id)
print("\nBusiness Recommendations:")
for recommendation in recommendations:
    print("-", recommendation)