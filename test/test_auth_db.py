import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.auth_db import get_company_details
company_id = 1
company = get_company_details(company_id)
print("Company Details:", company)