from .connection_db import connect_db
from .auth_db import login_user, register_company, get_company_details
from .products_db import (get_products, get_product_by_id, get_low_stock_products, add_product, update_product, delete_product)
from .dealers_db import (add_dealer, delete_dealer, get_dealer_by_id, get_dealers, update_dealer,)
from .purchases_db import add_purchase, get_purchase_orders
from .sales_db import (add_sales_order, get_sales_orders, get_sales_data_for_ml)
from .demand_prediction_db import save_demand_prediction, get_demand_predictions
from .sales_prediction_db import save_sales_prediction, get_sales_predictions

__all__ = [
    "connect_db",
    "login_user",
    "register_company",
    "get_company_details",
    "add_product",
    "delete_product",
    "get_product_by_id",
    "get_products",
    "update_product",
    "add_dealer",
    "delete_dealer",
    "get_dealer_by_id",
    "get_dealers",
    "update_dealer",
    "add_purchase",
    "get_purchase_orders",
    "add_sales_order",
    "get_sales_orders",
    "get_sales_data_for_ml",
    "save_demand_prediction",
    "get_demand_predictions",
    "save_sales_prediction",
    "get_sales_predictions",
]

