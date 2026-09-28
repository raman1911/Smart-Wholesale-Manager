import streamlit as st
from database.dealers_db import (add_dealer, delete_dealer, get_dealers, update_dealer)

def dealers_page(comapny_id):
    st.title("🤝 Dealers Management")

    user = st.session_state.get("user")
    company_id = user.get("company_id") if user else None

    if not company_id:
        st.warning("Company context is missing. Please login again.")
        return

    dealers = get_dealers(company_id)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Add Dealer", "View Dealers", "Update Dealer", "Delete Dealer"]
    )

    with tab1:
        with st.form("add_dealer_form"):
            dealer_name = st.text_input("Dealer Name")
            contact_person = st.text_input("Contact Person")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            gst_number = st.text_input("GST Number")
            address = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            submitted = st.form_submit_button("Add Dealer")

        if submitted:
            if not dealer_name.strip():
                st.warning("Dealer Name is required.")
            else:
                dealer_id = add_dealer(
                    company_id,
                    dealer_name.strip(),
                    contact_person.strip(),
                    phone.strip(),
                    email.strip(),
                    gst_number.strip(),
                    address.strip(),
                    city.strip(),
                    state.strip(),
                )
                if dealer_id:
                    st.success("Dealer added successfully.")
                    st.rerun()

                else:
                    st.error("Dealer already exists or unable to add dealer.")

    with tab2:
        view_query = st.text_input("Search dealers by name, contact person, or email", key="view_dealer_search")
        filtered_dealers = get_dealers(company_id, search=view_query) if view_query else dealers

        if filtered_dealers:
            st.dataframe(
                filtered_dealers, 
                use_container_width=True
                )
            
        else:
            st.info("No dealers found for your search.")

    with tab3:
        if not dealers:
            st.info("No dealers available yet. Add a dealer first.")

        else:
            dealer_choices = {f"{d['dealer_id']} - {d['dealer_name']}": d for d in dealers}
            selected_key = st.selectbox("Select dealer to update", list(dealer_choices.keys()))
            selected_dealer = dealer_choices[selected_key]

            with st.form("update_dealer_form"):
                dealer_name = st.text_input("Dealer Name", value=selected_dealer["dealer_name"])
                contact_person = st.text_input("Contact Person", value=selected_dealer.get("contact_person", ""))
                phone = st.text_input("Phone", value=selected_dealer.get("phone", ""))
                email = st.text_input("Email", value=selected_dealer.get("email", ""))
                gst_number = st.text_input("GST Number", value=selected_dealer.get("gst_number", ""))
                address = st.text_area("Address", value=selected_dealer.get("address", ""))
                city = st.text_input("City", value=selected_dealer.get("city", ""))
                state = st.text_input("State", value=selected_dealer.get("state", ""))
                submitted = st.form_submit_button("Update Dealer")

            if submitted:
                updated = update_dealer(
                    selected_dealer["dealer_id"],
                    company_id,
                    dealer_name.strip(),
                    contact_person.strip(),
                    phone.strip(),
                    email.strip(),
                    gst_number.strip(),
                    address.strip(),
                    city.strip(),
                    state.strip(),
                )
                if updated:
                    st.success("Dealer updated successfully.")
                    st.rerun()
                else:
                    st.error("Unable to update dealer.")

    with tab4:
        if not dealers:
            st.info("No dealers available yet. Add a dealer first.")
        else:
            delete_query = st.text_input("Search dealer to delete", key="delete_dealer_search")
            delete_candidates = [
                d
                for d in dealers
                if not delete_query
                or delete_query.lower() in d["dealer_name"].lower()
                or delete_query.lower() in (d.get("email") or "").lower()
                or delete_query.lower() in (d.get("contact_person") or "").lower()
            ]

            delete_options = {f"{d['dealer_id']} - {d['dealer_name']}": d for d in delete_candidates}
            if delete_options:
                selected_key = st.selectbox("Choose dealer", list(delete_options.keys()))
                if st.button("Delete Dealer"):
                    deleted = delete_dealer(delete_options[selected_key]["dealer_id"], company_id)
                    if deleted:
                        st.success("Dealer deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Unable to delete dealer.")
            else:
                st.info("No dealers found for your search.")    