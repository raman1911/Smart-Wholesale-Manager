import streamlit as st
from database.products_db import (add_product, delete_product, get_products, update_product, get_low_stock_products)

def products_page(comapany_id):
    st.title("📦Product Management")

    user = st.session_state.get("user")
    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context is missing. Please login again.")
        return

    low_stock = get_low_stock_products(company_id)

    if low_stock:
        st.warning(f"⚠️ {len(low_stock)} products are low in stock")

    products = get_products(company_id)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Add Product", "View Products", "Update Product", "Delete Product"]
    )

    with tab1:
        with st.form("add_product_form"):
            product_name = st.text_input("Product Name")
            category = st.text_input("Category")
            brand = st.text_input("Brand")
            unit = st.text_input("Unit")
            purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01, format="%.2f")
            selling_price = st.number_input("Selling Price", min_value=0.0, step=0.01, format="%.2f")
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1, value=0)
            minimum_stock = st.number_input("Minimum Stock", min_value=0, step=1, value=0)
            description = st.text_area("Description")
            submitted = st.form_submit_button("Add Product")

        if submitted:
            if not product_name.strip():
                st.warning("Product Name is required.")
            else:
                product_id = add_product(
                    company_id,
                    product_name.strip(),
                    category.strip(),
                    brand.strip(),
                    unit.strip(),
                    purchase_price,
                    selling_price,
                    stock_quantity,
                    minimum_stock,
                    description.strip(),
                )
                if product_id:
                    st.success("Product added successfully.")
                    st.rerun()
                else:
                    st.error("Product already exists or unable to add product.")

    with tab2:
        view_query = st.text_input("Search products by name, category, or brand", key="view_product_search")
        filtered_products = get_products(company_id, search=view_query) if view_query else products

        if filtered_products:
            st.dataframe(filtered_products, use_container_width=True)
        else:
            st.info("No products found for your search.")

    with tab3:
        if not products:
            st.info("No products available yet. Add a product first.")

        else:
            product_choices = {f"{p['product_id']} - {p['product_name']}": p for p in products}
            selected_key = st.selectbox("Select product to update", list(product_choices.keys()))
            selected_product = product_choices[selected_key]

            with st.form("update_product_form"):
                product_name = st.text_input("Product Name", value=selected_product["product_name"])
                category = st.text_input("Category", value=selected_product.get("category", ""))
                brand = st.text_input("Brand", value=selected_product.get("brand", ""))
                unit = st.text_input("Unit", value=selected_product.get("unit", ""))
                purchase_price = st.number_input(
                    "Purchase Price",
                    min_value=0.0,
                    step=0.01,
                    value=float(selected_product.get("purchase_price") or 0.0),
                    format="%.2f",
                )
                selling_price = st.number_input(
                    "Selling Price",
                    min_value=0.0,
                    step=0.01,
                    value=float(selected_product.get("selling_price") or 0.0),
                    format="%.2f",
                )
                stock_quantity = st.number_input(
                    "Stock Quantity",
                    min_value=0,
                    step=1,
                    value=int(selected_product.get("stock_quantity") or 0),
                )
                minimum_stock = st.number_input(
                    "Minimum Stock",
                    min_value=0,
                    step=1,
                    value=int(selected_product.get("minimum_stock") or 0),
                )
                description = st.text_area("Description", value=selected_product.get("description", ""))
                submitted = st.form_submit_button("Update Product")

            if submitted:
                updated = update_product(
                    selected_product["product_id"],
                    company_id,
                    product_name.strip(),
                    category.strip(),
                    brand.strip(),
                    unit.strip(),
                    purchase_price,
                    selling_price,
                    stock_quantity,
                    minimum_stock,
                    description.strip(),
                )
                if updated:
                    st.success("Product updated successfully.")
                    st.rerun()
                else:
                    st.error("Unable to update product.")

    with tab4:
        if not products:
            st.info("No products available yet. Add a product first.")
        else:
            delete_query = st.text_input("Search product to delete", key="delete_product_search")
            delete_candidates = [
                p
                for p in products
                if not delete_query
                or delete_query.lower() in p["product_name"].lower()
                or delete_query.lower() in (p.get("category") or "").lower()
                or delete_query.lower() in (p.get("brand") or "").lower()
            ]

            delete_options = {f"{p['product_id']} - {p['product_name']}": p for p in delete_candidates}
            if delete_options:
                selected_key = st.selectbox("Choose product", list(delete_options.keys()))
                if st.button("Delete Product"):
                    deleted = delete_product(delete_options[selected_key]["product_id"], company_id)
                    if deleted:
                        st.success("Product deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Unable to delete product.")
            else:
                st.info("No products found for your search.")