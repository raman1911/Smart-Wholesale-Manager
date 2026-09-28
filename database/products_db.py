from .utils_db import _fetch_all, _fetch_one, _execute_commit

def product_exists(company_id, product_name):
    query = """SELECT product_id FROM products WHERE company_id=%s AND product_name=%s"""
    return _fetch_one(query,(company_id, product_name))

def get_products(company_id, search=""):
    query = """ SELECT * FROM products WHERE company_id=%s"""
    params = [company_id]

    if search:
        query += """ AND product_name LIKE %s"""
        params.append("%" + search + "%")

    query += """ ORDER BY product_id ASC"""

    return _fetch_all(query, params)

def get_product_by_id(product_id, company_id):
    query = """SELECT * FROM products WHERE product_id=%s AND company_id=%s"""
    return _fetch_one(query, (product_id, company_id))

def add_product(company_id, product_name, category, brand, unit, purchase_price, selling_price, stock_quantity, minimum_stock, description):
    if product_exists(company_id, product_name):
        return False

    query = """INSERT INTO products(company_id, product_name, category, brand, unit, purchase_price, selling_price, stock_quantity, minimum_stock, description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    return _execute_commit(query, (company_id, product_name, category, brand, unit, purchase_price, selling_price, stock_quantity, minimum_stock, description), fetch_lastrow=True)

def update_product(product_id, company_id, product_name, category, brand, unit, purchase_price, selling_price, stock_quantity, minimum_stock, description):
    query = """UPDATE products
    SET product_name=%s, category=%s, brand=%s, unit=%s, purchase_price=%s, selling_price=%s, stock_quantity=%s, minimum_stock=%s, description=%s
    WHERE product_id=%s AND company_id=%s
    """

    return _execute_commit(query, (product_name, category, brand, unit, purchase_price, selling_price, stock_quantity, minimum_stock, description, product_id, company_id))

def delete_product(product_id, company_id):
    query = """DELETE FROM products WHERE product_id=%s AND company_id=%s"""
    return _execute_commit(query, (product_id, company_id))

def get_low_stock_products(company_id):
    query = """SELECT * FROM products
    WHERE company_id=%s AND stock_quantity <= minimum_stock 
    ORDER BY stock_quantity ASC"""

    return _fetch_all(query, (company_id,))