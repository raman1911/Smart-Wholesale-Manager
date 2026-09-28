import streamlit as st
import pandas as pd

from database import ( get_sales_orders, get_purchase_orders, get_products, get_dealers)

def reports_page(company_id):
    st.title("📊 Business Reports")
    st.caption("Detailed sales, purchase, inventory and profit analysis")

    user = st.session_state.get("user")
    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context missing. Please login again.")
        return

    sales = get_sales_orders(company_id)
    purchases = get_purchase_orders(company_id)
    products = get_products(company_id)
    dealers = get_dealers(company_id)

    sales_df = pd.DataFrame(sales)
    purchase_df = pd.DataFrame(purchases)
    product_df = pd.DataFrame(products)
    dealer_df = pd.DataFrame(dealers)
   
    tab1, tab2, tab3, tab4 = st.tabs(["Sales Report", "Purchase Report", "Inventory Report", "Profit Report"])

    with tab1:
        st.subheader("Sales Report")

        if sales_df.empty:
            st.info("No sales data available.")

        else:
            total_revenue = (sales_df["total_amount"].sum())
            total_quantity = (sales_df["quantity"].sum())
            total_orders = len(sales_df)
            average_order = (total_revenue / total_orders if total_orders > 0 else 0)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Revenue", f"₹ {total_revenue:,.2f}")

            with col2:
                st.metric("Items Sold", total_quantity)

            with col3:
                st.metric("Total Orders", total_orders)

            with col4:
                st.metric("Avg Order Value", f"₹ {average_order:,.2f}")

            st.divider()

            st.subheader("Product Wise Sales")

            product_sales = (
                sales_df.groupby("product_name") ["quantity"].sum().sort_values(ascending=False)
            )

            st.bar_chart( product_sales)

            st.divider()

            st.subheader("Top Selling Products")

            top_products = (product_sales.head(5).reset_index())
            top_products.columns = ["Product", "Quantity Sold"]

            st.dataframe(top_products, use_container_width=True)

            st.divider()

            st.subheader("Complete Sales Records")

            st.dataframe(sales_df, use_container_width=True)

    with tab2:
        st.subheader("Purchase Report")

        if purchase_df.empty:
            st.info("No purchase data available.")

        else:
            total_purchase = (purchase_df["total_amount"].sum())
            total_quantity = (purchase_df["quantity"].sum())
            total_orders = len(purchase_df)
            average_purchase = (total_purchase / total_orders if total_orders > 0 else 0)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Purchase", f"₹ {total_purchase:,.2f}")

            with col2:
                st.metric("Items Purchased", total_quantity)

            with col3:
                st.metric("Purchase Orders", total_orders)

            with col4:
                st.metric("Avg Purchase Value", f"₹ {average_purchase:,.2f}")

            st.divider()

            st.subheader( "Dealer Wise Purchase")

            if "dealer_name" in purchase_df.columns:
                dealer_purchase = (purchase_df.groupby("dealer_name")["total_amount"].sum().sort_values(ascending=False))
                st.bar_chart(dealer_purchase)

            else:
                st.warning("Dealer information not available.")

            st.divider()
            
            st.subheader("Product Wise Purchase")

            if "product_name" in purchase_df.columns:
                product_purchase = (purchase_df.groupby("product_name") ["quantity"].sum().sort_values(ascending=False))
                st.bar_chart(product_purchase)

            else:
                st.warning("Product information not available.")

            st.divider()

            st.subheader("Top Suppliers")

            if "dealer_name" in purchase_df.columns:
                top_dealers = (dealer_purchase.head(5).reset_index())
                top_dealers.columns = ["Dealer", "Purchase Amount"]

                st.dataframe(top_dealers, use_container_width=True)

            st.divider()

            st.subheader("Complete Purchase Records")

            st.dataframe(purchase_df, use_container_width=True)

    with tab3:
        st.subheader("Inventory Intelligence")

        if product_df.empty:
            st.info("No product data available.")

        else:
            total_products = len(product_df)
            total_stock = (product_df["stock_quantity"].sum())
            low_stock = product_df[product_df["stock_quantity"] <= product_df["minimum_stock"]]
            out_of_stock = product_df[product_df["stock_quantity"] <= 0]

            health_score = 100
            health_score -= (len(low_stock) * 5)
            health_score -= (len(out_of_stock) * 10)

            if health_score < 0:
                health_score = 0

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Products", total_products)

            with col2:
                st.metric("Stock Units", total_stock)

            with col3:
                st.metric("Inventory Health", f"{health_score}%")

            st.divider()

            st.subheader("AI Inventory Recommendations")

            if len(out_of_stock) > 0:
                st.error(f"""AI Alert: {len(out_of_stock)} products are out of stock. Immediate restocking is recommended.""")

            elif len(low_stock) > 0:
                st.warning(f"""AI Alert: {len(low_stock)} products have low stock. Consider placing purchase orders soon.""")

            else:
                st.success("""AI Analysis: Inventory level is healthy. No immediate action required.""")

            st.divider()

            st.subheader("AI Stock Risk Detection")

            if not low_stock.empty:
                st.dataframe(
                    low_stock[["product_name", "stock_quantity", "minimum_stock"]], use_container_width=True
                )

            else:
                st.success("No risky products detected.")

            st.divider()

            st.subheader("Stock Distribution")

            stock_chart = (product_df.set_index("product_name")["stock_quantity"])

            st.bar_chart(stock_chart)

    with tab4:
        st.subheader("AI Profit Analysis")

        if sales_df.empty or purchase_df.empty:
            st.info("Need sales and purchase data for profit analysis.")

        else:
            total_revenue = (sales_df["total_amount"].sum())
            total_cost = (purchase_df["total_amount"].sum())
            profit = (total_revenue - total_cost)

            profit_margin = 0

            if total_revenue > 0:
                profit_margin = (profit / total_revenue) * 100

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Revenue", f"₹ {total_revenue:,.2f}")

            with col2:
                st.metric("Purchase Cost", f"₹ {total_cost:,.2f}")

            with col3:
                st.metric("Profit", f"₹ {profit:,.2f}")

            col4, col5 = st.columns(2)

            with col4:
                st.metric("Profit Margin", f"{profit_margin:.2f}%")

            with col5:
                if profit_margin >= 30:
                    status = "Excellent"

                elif profit_margin >= 10:
                    status = "Good"

                else:
                    status = "Needs Improvement"

                st.metric("AI Business Status", status)

            st.divider()

            st.subheader("AI Profit Recommendations")

            if profit < 0:
                st.error(
                    """
                    AI Alert:
                    Business is running in loss.

                    Suggestions:
                    • Reduce unnecessary purchase cost
                    • Review product pricing
                    • Focus on high-margin products
                    """
                )

            elif profit_margin < 10:
                st.warning(
                    """
                    AI Suggestion:
                    Profit margin is low.

                    Consider:
                    • Increasing selling price
                    • Negotiating supplier prices
                    • Promoting profitable products
                    """
                )

            else:
                st.success(
                    """
                    AI Analysis:
                    Business profitability looks healthy.

                    Continue monitoring growth trends.
                    """
                )

            st.divider()

            st.subheader("Product Revenue Analysis")

            if "product_name" in sales_df.columns:
                product_profit = (sales_df.groupby("product_name") ["total_amount"].sum().sort_values(ascending=False))

                st.bar_chart(product_profit)

            else:
                st.info("Product information not available.")

