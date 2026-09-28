import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.products_db import get_products
company_id = 1
products = get_products(company_id)
print("Total Products Found:", len(products))
print(products)