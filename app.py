import streamlit as st

from authentication.login import login_page
from authentication.registration import registration_page
from dashboard.dashboard import dashboard_page

st.set_page_config(
    page_title="AI Wholesale Management System",
    page_icon="📦",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.logged_in:
    dashboard_page()

else:
    if st.session_state.page == "login":
        login_page()

        st.divider()
        
        if st.button("Create New Company"):
            st.session_state.page = "registration"
            st.rerun()

    elif st.session_state.page == "registration":
        registration_page()

        st.divider()

        if st.button("Already have account? Login"):
            st.session_state.page = "login"
            st.rerun()