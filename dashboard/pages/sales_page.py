import streamlit as st
from datetime import date

from database import get_products
from database.auth_db import get_company_details
from database.sales_db import add_sales_order, get_sales_orders

from utils.bill_pdf import save_bill_pdf

def sales_page(company_id):
    st.title("💰 Sales Management")

    if "sale_items" not in st.session_state:
        st.session_state.sale_items = []

    user = st.session_state.get("user")
    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context is missing. Please login again.")
        return

    products = get_products(company_id)

    tab1, tab2, tab3 = st.tabs(["Sales Entry", "Sales History", "Saved Bills"])

    with tab1:
        if not products:
            st.warning("Please add products before creating sales.")
            return

        st.subheader("Customer Details")

        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.text_input("Customer Name", key="sale_customer_name")

        with col2:
            customer_phone = st.text_input("Customer Phone", key="sale_customer_phone")

        sale_date = st.date_input("Sale Date", value=date.today(), key="sale_date")

        st.divider()

        st.subheader("Add Products")

        product_options = {
            f"{p['product_id']} - {p['product_name']}": p
            for p in products
        }

        selected_product = st.selectbox(
            "Product",
            list(product_options.keys()),
            key="selected_sale_product"
        )

        selected_product_data = product_options[selected_product]
        product_id = selected_product_data["product_id"]
        default_price = float(selected_product_data.get("selling_price", 0.0))

        col1, col2 = st.columns(2)

        with col1:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                step=1,
                value=1,
                key="sale_quantity"
            )

        with col2:
            selling_price = st.number_input(
                "Selling Price",
                min_value=0.0,
                step=0.01,
                value=default_price,
                key="sale_selling_price"
            )

        item_total = quantity * selling_price
        st.info(f"Item Total: ₹ {item_total:,.2f}")

        if st.button("Add Item", use_container_width=True):
            if quantity <= 0:
                st.warning("Quantity must be greater than zero.")
            elif selling_price <= 0:
                st.warning("Selling price must be greater than zero.")
            else:
                item = {
                    "product_id": product_id,
                    "product_name": selected_product_data["product_name"],
                    "quantity": quantity,
                    "selling_price": selling_price,
                    "total_amount": item_total
                }
                st.session_state.sale_items.append(item)
                st.success(f"{selected_product_data['product_name']} added to bill")
                st.rerun()

        if st.session_state.sale_items:
            st.divider()
            st.subheader("Current Bill")

            grand_total = 0

            for index, item in enumerate(st.session_state.sale_items):
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1.5, 1.5, 0.7])

                with col1:
                    st.write(item["product_name"])

                with col2:
                    st.write(item["quantity"])

                with col3:
                    st.write(f"₹ {item['selling_price']:,.2f}")

                with col4:
                    st.write(f"₹ {item['total_amount']:,.2f}")

                with col5:
                    if st.button("❌", key=f"remove_item_{index}"):
                        st.session_state.sale_items.pop(index)
                        st.rerun()

                grand_total += item["total_amount"]

            st.divider()
            st.subheader(f"Grand Total: ₹ {grand_total:,.2f}")

            if st.button("Complete Sale", type="primary", use_container_width=True):
                if not customer_name.strip():
                    st.warning("Customer name is required.")
                elif not customer_phone.strip():
                    st.warning("Customer phone is required.")
                else:
                    result = add_sales_order(
                        company_id=company_id,
                        customer_name=customer_name.strip(),
                        customer_phone=customer_phone.strip(),
                        sale_date=sale_date,
                        items=st.session_state.sale_items.copy()
                    )

                    if result and result.get("status") == "SUCCESS":
                        bill_number = result["bill_number"]
                        st.success("Sale saved successfully!")
                        st.success(f"Bill Number: {bill_number}")
                        st.success(f"Total: ₹ {result['grand_total']:,.2f}")

                        invoice_rows = []
                        for item in st.session_state.sale_items:
                            invoice_rows.append({
                                "bill_number": bill_number,
                                "sale_date": str(sale_date),
                                "customer_name": customer_name.strip(),
                                "customer_phone": customer_phone.strip(),
                                "product_name": item["product_name"],
                                "quantity": item["quantity"],
                                "selling_price": item["selling_price"],
                                "total_amount": item["total_amount"],
                                "unit": "pcs",
                            })

                        company = get_company_details(company_id)
                        pdf_path, pdf_bytes = save_bill_pdf(
                            company_id,
                            bill_number,
                            company,
                            invoice_rows
                        )

                        st.session_state.last_saved_bill = bill_number
                        st.session_state.sale_items = []

                        st.success("Invoice PDF generated for printing.")
                        st.download_button(
                            label="Print / Download Invoice PDF",
                            data=pdf_bytes,
                            file_name=f"{bill_number}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                    elif result and result.get("status") == "INSUFFICIENT_STOCK":
                        st.error(
                            f"Insufficient stock for {result['product_name']}. "
                            f"Available: {result['available']}, Requested: {result['requested']}."
                        )

                    elif result and result.get("status") == "PRODUCT_NOT_FOUND":
                        st.error(f"Product not found: {result['product_name']}")

                    elif result and result.get("status") == "ERROR":
                        st.error(f"Sale could not be saved: {result['message']}")

                    else:
                        st.error("Sale could not be saved.")

    with tab2:
        search = st.text_input(
            "Search sales by bill number, customer name, phone, or product",
            key="sales_search"
        )

        sales_orders = get_sales_orders(company_id, search=search)

        if sales_orders:
            st.dataframe(sales_orders, use_container_width=True)
        else:
            st.info("No sales records found.")

    with tab3:
        st.subheader("Saved Bills")

        sales_history = get_sales_orders(company_id)

        if sales_history:
            seen_bill_numbers = set()
            bill_lists = []

            for row in sales_history:
                bill_number = row.get("bill_number")
                if bill_number and bill_number not in seen_bill_numbers:
                    seen_bill_numbers.add(bill_number)
                    bill_lists.append({
                        "bill_number": bill_number,
                        "customer_name": row.get("customer_name"),
                        "customer_phone": row.get("customer_phone"),
                        "sale_date": row.get("sale_date"),
                    })

            st.dataframe(
                [
                    {
                        "Bill Number": row["bill_number"],
                        "Customer": row.get("customer_name"),
                        "Phone": row.get("customer_phone"),
                        "Date": row.get("sale_date")
                    }
                    for row in bill_lists
                ],
                use_container_width=True,
                hide_index=True,
            )

            selected_bill = st.selectbox(
                "Select Saved Invoice",
                [row["bill_number"] for row in bill_lists],
                key="selected_saved_bill_pdf"
            )

            bill_rows = [
                item for item in sales_history if item.get("bill_number") == selected_bill
            ]

            if bill_rows:
                company = get_company_details(company_id)
                _, pdf_bytes = save_bill_pdf(company_id, selected_bill, company, bill_rows)

                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label=f"⬇Download {selected_bill}.pdf",
                        data=pdf_bytes,
                        file_name=f"{selected_bill}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

                with col2:
                    preview_clicked = st.button(
                        "👁️ View Invoice",
                        key=f"view_invoice_{selected_bill}",
                        use_container_width=True,
                    )

                if preview_clicked:
                    company = get_company_details(company_id)
                    invoice_html = [
                        "<div style='font-family: Arial, sans-serif; background: white; border: 1px solid #dfe3e8; border-radius: 12px; padding: 24px; color: #1f2937; max-width: 900px;'>",
                        f"<div style='text-align:center; font-size: 28px; font-weight: bold; margin-bottom: 8px;'>{company.get('company_name') or 'Wholesale Business'}</div>",
                        f"<div style='text-align:center; font-size: 14px; color: #4b5563; margin-bottom: 18px;'>{(company.get('address') or '') + (' , ' + (company.get('city') or '')) if company.get('address') or company.get('city') else ''}</div>",
                        "<hr style='border: 1px solid #e5e7eb; margin: 12px 0 18px 0;'>",
                        "<div style='display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;'>",
                        f"<div><b>Bill No:</b> {selected_bill}</div>",
                        f"<div><b>Date:</b> {bill_rows[0].get('sale_date') or 'N/A'}</div>",
                        f"<div><b>Customer:</b> {bill_rows[0].get('customer_name') or '-'}</div>",
                        f"<div><b>Phone:</b> {bill_rows[0].get('customer_phone') or '-'}</div>",
                        "</div>",
                        "<table style='width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px;'>",
                        "<thead><tr style='background:#f3f4f6;'><th style='padding:10px; border:1px solid #dfe3e8; text-align:left;'>Product</th><th style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>Qty</th><th style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>Rate</th><th style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>Amount</th></tr></thead>",
                        "<tbody>"
                    ]

                    total_amount = 0
                    for item in bill_rows:
                        invoice_html.append(
                            "<tr>"
                            f"<td style='padding:10px; border:1px solid #dfe3e8;'>{item.get('product_name') or 'Product'}</td>"
                            f"<td style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>{item.get('quantity') or 0}</td>"
                            f"<td style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>₹ {float(item.get('selling_price', 0) or 0):,.2f}</td>"
                            f"<td style='padding:10px; border:1px solid #dfe3e8; text-align:right;'>₹ {float(item.get('total_amount', 0) or 0):,.2f}</td>"
                            "</tr>"
                        )
                        total_amount += float(item.get('total_amount', 0) or 0)

                    invoice_html.extend([
                        "</tbody>",
                        "</table>",
                        "<div style='margin-top: 18px; display: flex; justify-content: flex-end;'>",
                        f"<div style='width: 280px; border: 1px solid #dfe3e8; border-radius: 10px; padding: 12px; background: #fafafa;'>",
                        f"<div style='display:flex; justify-content:space-between; margin-bottom:8px;'><span>Subtotal</span><span>₹ {total_amount:,.2f}</span></div>",
                        f"<div style='display:flex; justify-content:space-between; margin-bottom:8px;'><span>Total Items</span><span>{len(bill_rows)}</span></div>",
                        f"<div style='display:flex; justify-content:space-between; font-weight:bold; font-size:16px;'><span>Grand Total</span><span>₹ {total_amount:,.2f}</span></div>",
                        "</div>",
                        "</div>",
                        "<div style='margin-top: 22px; text-align:center; color:#6b7280; font-size: 12px;'>Thank you for your business.</div>",
                        "</div>"
                    ])

                    st.markdown("\n".join(invoice_html), unsafe_allow_html=True)

                st.info("Use View Invoice to preview the bill, or download it to print.")
        else:
            st.info("No saved bills found.")