import streamlit as st
from datetime import date

from database import (add_purchase, get_dealers, get_products, get_purchase_orders)

def purchase_page(compaany_id):
    st.title("🛒 Purchase Management")

    user = st.session_state.get("user")
    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context is missing. Please login again.")
        return

    products = get_products(company_id)
    dealers = get_dealers(company_id)

    tab1, tab2 = st.tabs(["Purchase Entry", "Purchase History"])

    with tab1:
        if not products or not dealers:
            st.warning("Please add at least one product and one dealer before creating a purchase entry.")

        else:
            with st.form("add_order_form"):
                bill_number = st.text_input("Bill Number")
                dealer_key = st.selectbox("Dealer",[f"{d['dealer_id']} - {d['dealer_name']}"for d in dealers])
                product_key = st.selectbox("Product", [f"{p['product_id']} - {p['product_name']}" for p in products])
                quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
                purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01, format="%.2f")

                total_amount = quantity * purchase_price
                st.info(f"Total Amount: ₹ {total_amount:,.2f}")

                purchase_date = st.date_input("Purchase Date", value=date.today())

                submitted = st.form_submit_button("Add Purchase")

            if submitted:
                selected_product_id = int(product_key.split(" - ")[0])
                selected_dealer_id = int(dealer_key.split(" - ")[0])

                if not bill_number.strip():
                    st.warning("Bill Number is required.")

                elif quantity <= 0:
                    st.warning("Quantity must be greater than zero.")

                elif purchase_price <= 0:
                    st.warning("Purchase price must be greater than zero.")

                else:
                    purchase_id = add_purchase(
                        company_id,
                        selected_dealer_id,
                        selected_product_id,
                        bill_number.strip(),
                        quantity,
                        purchase_price,
                        purchase_date
                    )

                    if purchase_id:
                        st.success("Purchase order added successfully.")
                        st.rerun()

                    elif purchase_id is False:
                        st.error("Bill number already exists.")

                    else:
                        st.error("Unable to add purchase order.")

    with tab2:
        view_query = st.text_input(
            "Search orders by bill number, dealer name, or product name",
            key="view_order_search"
        )

        purchase_orders = get_purchase_orders(
            company_id,
            search=view_query
        )

        if purchase_orders:
            st.dataframe(purchase_orders, use_container_width=True)

        else:
            st.info("No purchase orders found.")