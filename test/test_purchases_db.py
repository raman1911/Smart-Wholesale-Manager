import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.purchases_db import get_purchase_orders
company_id = 1
purchases = get_purchase_orders(company_id)
print("Total Purchase Orders Found:", len(purchases))
print(purchases)