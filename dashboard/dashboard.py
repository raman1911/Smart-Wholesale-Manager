import streamlit as st

from dashboard.pages.home_page import home_page
from dashboard.pages.products_page import products_page
from dashboard.pages.dealers_page import dealers_page
from dashboard.pages.purchases_page import purchase_page
from dashboard.pages.sales_page import sales_page
from dashboard.pages.reports_page import reports_page
from dashboard.pages.business_analytics_page import business_analytics_page

def dashboard_page():

    user = st.session_state.user
    company_id = user["company_id"]

    st.sidebar.title("📦 Smart Wholesale Manager")

    st.sidebar.divider()

    user = st.session_state.user
    st.sidebar.subheader("👤 User Profile")
    st.sidebar.write(f"Username: **{user['username']}**")
    st.sidebar.write(f"Role: **{user['role']}**")

    st.sidebar.divider()

    st.sidebar.subheader("🚀 Navigation")
    menu = st.sidebar.radio( "Select Option", ("🏠 Home", "📦 Products", "🤝 Dealers", "🛒 Purchase", "💰 Sales", "🔍 Business Analytics", "📊 Reports", "🚪 Logout"))

    if menu == "🏠 Home":
        home_page(company_id)

    elif menu == "📦 Products":
        products_page(company_id)

    elif menu == "🤝 Dealers":
        dealers_page(company_id)

    elif menu == "🛒 Purchase":
        purchase_page(company_id)

    elif menu == "💰 Sales":
        sales_page(company_id)

    elif menu == "📊 Reports":
        reports_page(company_id)

    elif menu == "🔍 Business Analytics":
        business_analytics_page(company_id)

    elif menu == "🚪 Logout":

        st.session_state.logged_in = False
        st.session_state.user = None

        st.success("Logged out successfully.")
        st.rerun()
