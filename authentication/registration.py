import streamlit as st
from database.auth_db import register_company


def registration_page():
    st.subheader("Company Registration")

    with st.form("registration_form"):

        st.write("Company Details")

        company_name = st.text_input("Company Name")
        owner_name = st.text_input("Owner Name")

        business_type = st.selectbox(
            "Business Type",
            [
                "General Wholesale",
                "Grocery",
                "Electronics",
                "Medical",
                "Hardware",
                "Other"
            ]
        )

        gst_number = st.text_input("GST Number (Optional)")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        address = st.text_area("Address")
        city = st.text_input("City")
        state = st.text_input("State")
        pincode = st.text_input("Pincode")

        st.write("Admin Account")

        username = st.text_input("Create Username")
        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Register Company"
        )

    if submitted:
        company_name = company_name.strip()
        owner_name = owner_name.strip()
        gst_number = gst_number.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()
        city = city.strip()
        state = state.strip()
        pincode = pincode.strip()
        username = username.strip()

        if company_name == "":
            st.warning("Please enter Company Name")

        elif owner_name == "":
            st.warning("Please enter Owner Name")

        elif address == "":
            st.warning("Please enter Address")

        elif phone == "":
            st.warning("Please enter Phone Number")

        elif username == "":
            st.warning("Please enter Username")

        elif password == "":
            st.warning("Please enter Password")

        elif password != confirm_password:
            st.error("Passwords do not match")

        else:
            registered, message = register_company(
                company_name,
                owner_name,
                business_type,
                gst_number,
                phone,
                email,
                address,
                city,
                state,
                pincode,
                username,
                password
            )

            if registered:
                st.success(message)
                st.session_state["page"] = "login"
                st.rerun()

            else:
                st.error(message)