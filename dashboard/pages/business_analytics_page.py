import streamlit as st
from datetime import date

from database import get_products
from database.auth_db import get_company_details
from database.demand_prediction_db import save_demand_prediction
from database.sales_prediction_db import save_sales_prediction

from ml_models.demand_prediction import predict_demand
from ml_models.sales_prediction import predict_sales
from ml_models.recommendation import generate_business_recommendations


def business_analytics_page(company_id):

    st.title("🔍 Business Analytics")
    st.write("Use AI and machine learning to understand sales, demand and inventory.")

    company = get_company_details(company_id)
    if not company:
        st.error("Company details not found.")
        return
    
    products = get_products(company_id)
    if not products:
        st.warning("No products available.")
        return

    product_options = {}
    for product in products:
        product_id = product["product_id"]
        product_name = product["product_name"]
        product_options[product_name] = product_id

    tab1, tab2, tab3, tab4 = st.tabs(["Demand Prediction", "Sales Forecast", "Recommendations", "Stock Alerts"])
    
    with tab1:
        st.subheader("Product Demand Prediction")
        st.write("Predict the expected quantity of a product for a future date.")

        selected_product = st.selectbox(
            "Select Product",
            list(product_options.keys()),
            key="demand_product"
        )

        prediction_date = st.date_input(
            "Select Prediction Date",
            value=date.today(),
            key="demand_date"
        )

        product_id = product_options[selected_product]

        if st.button("Predict Demand", key="predict_demand_button"):
            try:
                predicted_quantity = predict_demand(company_id, product_id, prediction_date.day, prediction_date.month, prediction_date.year)

                if predicted_quantity is None:
                    st.warning(
                        "Not enough historical sales data for this product. "
                        "At least 5 sales records are required."
                    )
                else:
                    st.success(f"Predicted Demand: {round(predicted_quantity)} units")
                    save_demand_prediction(company_id, product_id, prediction_date, round(predicted_quantity))
                    st.info(
                        f"For {selected_product} on "
                        f"{prediction_date.strftime('%d-%m-%Y')}"
                    )
            except Exception as e:
                st.error(f"Demand prediction failed: {e}")

    with tab2:
        st.subheader("Sales Revenue Forecast")
        st.write("Predict the expected sales revenue for a product on a future date.")

        selected_product = st.selectbox(
            "Select Product",
            list(product_options.keys()),
            key="sales_product"
        )

        prediction_date = st.date_input(
            "Select Prediction Date",
            value=date.today(),
            key="sales_date"
        )

        selling_price = st.number_input(
            "Selling Price",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="sales_price"
        )

        expected_quantity = st.number_input(
            "Expected Quantity",
            min_value=1,
            value=1,
            step=1,
            key="sales_quantity"
        )

        product_id = product_options[selected_product]

        if st.button("Forecast Sales", key="forecast_sales_button"):
            try:
                predicted_sales = predict_sales(company_id, product_id, prediction_date.day, prediction_date.month, prediction_date.year, selling_price)

                if predicted_sales is None:
                    st.warning(
                        "Not enough historical sales data for this product. "
                        "At least 5 sales records are required."
                    )
                else:
                    st.success(f"Expected Revenue: ₹{predicted_sales:,.2f}")
                    save_sales_prediction(company_id, product_id, prediction_date, expected_quantity, selling_price, predicted_sales)
                    st.info(
                        f"For {selected_product} on "
                        f"{prediction_date.strftime('%d-%m-%Y')}"
                    )

            except Exception as e:
                st.error(f"Sales forecasting failed: {e}")

    with tab3:
        st.subheader("Business Recommendations")
        st.write(
            "Analyze sales and inventory data to generate useful "
            "business recommendations."
        )

        if st.button("Generate Recommendations", key="recommendation_button"):
            try:
                recommendations = generate_business_recommendations(company_id)
                if recommendations:
                    for recommendation in recommendations:
                        st.info(f"{recommendation}")
                else:
                    st.success("No special recommendations at the moment.")

            except Exception as e:
                st.error(f"Could not generate recommendations: {e}")

    with tab4:
        st.subheader("Stock Alerts")
        st.write("Check products that may require restocking.")

        try:
            low_stock_products = []
            for product in products:
                product_name = product["product_name"]
                stock = product.get("stock_quantity", 0)

                if stock <= 10:
                    low_stock_products.append(
                        (product_name, stock)
                    )

            if low_stock_products:
                for product_name, stock in low_stock_products:
                    st.warning(
                        f"⚠️ {product_name} has only "
                        f"{stock} units in stock."
                    )

            else:
                st.success("No products currently have low stock.")

        except Exception as e:
            st.error(f"Could not check stock levels: {e}")