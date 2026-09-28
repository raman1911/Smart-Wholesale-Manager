import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.dealers_db import get_dealers
company_id = 1
dealers = get_dealers(company_id)
print("Total Dealers Found:", len(dealers))
print(dealers)