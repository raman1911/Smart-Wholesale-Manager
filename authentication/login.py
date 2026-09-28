import streamlit as st
from database.auth_db import login_user

def login_page():
    st.subheader("Login")

    with st.form("login_form"):

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

    if submitted:
        if username == "":
            st.warning("Please enter Username")

        elif password == "":
            st.warning("Please enter Password")

        else:
            user = login_user(username.strip(), password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user

                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Username or Password")