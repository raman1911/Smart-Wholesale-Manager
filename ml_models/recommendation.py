import pandas as pd
from database.sales_db import get_sales_data_for_ml
from database.products_db import get_products

def prepare_sales_analysis(company_id):
    df = get_sales_data_for_ml(company_id)
    if df is None or df.empty:
        return None
    return df

def get_best_selling_product(company_id):
    df = prepare_sales_analysis(company_id)

    if df is None or df.empty:
        return None

    product_sales = (df.groupby("product_name")["quantity"].sum().sort_values(ascending=False))

    if product_sales.empty:
        return None

    return product_sales.index[0]

def get_highest_revenue_product(company_id):
    df = prepare_sales_analysis(company_id)

    if df is None or df.empty:
        return None

    revenue = (df.groupby("product_name")["total_amount"].sum().sort_values(ascending=False))

    if revenue.empty:
        return None

    return revenue.index[0]

def get_stock_recommendations(company_id):
    products = get_products(company_id)
    if not products:
        return []

    product_df = pd.DataFrame(products)
    if product_df.empty:
        return []

    low_stock = product_df[product_df["stock_quantity"] <= product_df["minimum_stock"]]

    if low_stock.empty:
        return []

    return low_stock[["product_name", "stock_quantity", "minimum_stock"]].to_dict("records")

def generate_business_recommendations(company_id):

    recommendations = []
    best_product = get_best_selling_product(company_id)
    if best_product:
        recommendations.append(
            f"Increase stock of {best_product}. "
            f"It is the highest-selling product."
        )

    revenue_product = get_highest_revenue_product(company_id)
    if revenue_product:
        recommendations.append(
            f"Focus on {revenue_product}. "
            f"It generates the highest total revenue."
        )

    low_stock = get_stock_recommendations(company_id)
    for item in low_stock:
        recommendations.append(
            f"Restock {item['product_name']}. "
            f"Current stock: {item['stock_quantity']} "
            f"units, minimum required: {item['minimum_stock']} units."
        )

    if not recommendations:
        recommendations.append(
            "No urgent business recommendations "
            "were generated from the current data."
        )

    return recommendations