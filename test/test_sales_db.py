import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sales_db import get_sales_orders
company_id = 1
sales = get_sales_orders(company_id)
print("Total Sales Orders Found:", len(sales))
print(sales)