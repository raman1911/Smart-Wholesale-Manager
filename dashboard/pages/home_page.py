import streamlit as st
import pandas as pd

from database import (get_sales_orders, get_purchase_orders, get_products, get_dealers)

def home_page(company_id):

    st.title("📦 Smart Wholesale Manager")
    st.caption("Real-time business overview and management dashboard")

    user = st.session_state.get("user")

    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context is missing. Please login again.")
        return

    sales = get_sales_orders(company_id)
    purchases = get_purchase_orders(company_id)
    products = get_products(company_id)
    dealers = get_dealers(company_id)

    sales_df = pd.DataFrame(sales)
    purchase_df = pd.DataFrame(purchases)
    product_df = pd.DataFrame(products)
    dealers_df = pd.DataFrame(dealers)

    tab1, tab2, tab3 = st.tabs(["Business Summary", "Today's Business", "Business Alerts"])

    with tab1:

        st.subheader("Business Overview")

        total_sales = 0

        if not sales_df.empty:
            total_sales = sales_df["total_amount"].sum()

        total_purchase = 0

        if not purchase_df.empty:
            total_purchase = purchase_df["total_amount"].sum()

        estimated_profit = total_sales - total_purchase
        total_products = len(product_df)
        total_dealers = len(dealers_df)
        total_stock = 0

        if not product_df.empty:
            total_stock = product_df["stock_quantity"].sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Sales", f"₹ {total_sales:,.2f}")

        with col2:
            st.metric("Total Purchase", f"₹ {total_purchase:,.2f}")

        with col3:
            st.metric("Estimated Profit", f"₹ {estimated_profit:,.2f}")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric( "Products", total_products)

        with col5:
            st.metric("Dealers", total_dealers)

        with col6:
            st.metric("Stock Units", total_stock)

    with tab2:
        st.subheader("Today's Business")

        today = pd.Timestamp.today().date()
        today_sales_df = pd.DataFrame()
        total_today_sales = 0

        if not sales_df.empty:
            sales_dates = pd.to_datetime(sales_df["sale_date"]).dt.date
            today_sales_df = sales_df[sales_dates == today]
            total_today_sales = today_sales_df["total_amount"].sum()

        today_purchase_df = pd.DataFrame()
        total_today_purchase = 0

        if not purchase_df.empty:
            purchase_dates = pd.to_datetime(purchase_df["purchase_date"]).dt.date
            today_purchase_df = purchase_df[purchase_dates == today]
            total_today_purchase = today_purchase_df["total_amount"].sum()

        today_profit = (total_today_sales - total_today_purchase)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Today's Sales", f"₹ {total_today_sales:,.2f}")

        with col2:
            st.metric("Today's Purchase", f"₹ {total_today_purchase:,.2f}")

        with col3:
            st.metric("Today's Profit", f"₹ {today_profit:,.2f}")

        st.divider()

        st.subheader("Recent Sales")

        if not sales_df.empty:
            recent_sales = sales_df.sort_values(by="sale_date", ascending=False).head(5)

            st.dataframe(
                recent_sales[[ "bill_number", "customer_name", "product_name", "quantity", "total_amount", "sale_date"]],
                use_container_width=True
            )

        else:
            st.info("No sales records available.")

        st.divider()

        st.subheader("Recent Purchases")

        if not purchase_df.empty:
            recent_purchase = purchase_df.sort_values(by="purchase_date", ascending=False).head(5)

            st.dataframe(
                recent_purchase[
                    ["purchase_date", "dealer_name", "product_name", "quantity", "total_amount"]],
                use_container_width=True
            )

        else:
            st.info("No purchase records available.")

    with tab3:
        st.subheader("Business Alerts")

        st.write("### Inventory Alerts")

        if not product_df.empty:
            low_stock = product_df[product_df["stock_quantity"] <= product_df["minimum_stock"]]
            out_of_stock = product_df[product_df["stock_quantity"] <= 0]

            col1, col2 = st.columns(2)

            with col1:
                if len(low_stock) > 0:
                    st.warning(f"{len(low_stock)} products are low in stock.")

                else:
                    st.success("Stock level is healthy.")

            with col2:
                if len(out_of_stock) > 0:
                    st.error(f"{len(out_of_stock)} products are out of stock.")

                else:
                    st.success("Stock level is healthy.")

            if not low_stock.empty:
                st.write("### Low Stock Products")

                st.dataframe(
                    low_stock[["product_name", "stock_quantity", "minimum_stock"]],
                    use_container_width=True
                )

        else:
            st.info("No product data available.")

        st.divider()

        st.write("### Sales Performance")

        if not sales_df.empty:
            best_selling_product = (sales_df.groupby("product_name")["quantity"].sum().idxmax())
            highest_revenue_product = (sales_df.groupby("product_name")["total_amount"].sum().idxmax())

            col1, col2 = st.columns(2)

            with col1:
                st.success(f"Best Selling Product:\n\n{best_selling_product}")

            with col2:
                st.info(f"Highest Revenue Product:\n\n{highest_revenue_product}")

        else:
            st.info("No sales data available.")

        st.divider()

        st.write("### Business Status")

        if estimated_profit > 0:
            st.success("Business is running in profit.")

        elif estimated_profit < 0:
            st.warning("Business is currently in loss.")

        else:
            st.info("Not enough data for business evaluation.")