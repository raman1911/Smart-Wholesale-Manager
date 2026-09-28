from .utils_db import _execute_commit, _fetch_all, _fetch_one

def dealer_exists(company_id, dealer_name):
    query = """SELECT dealer_id FROM dealers WHERE company_id=%s AND dealer_name=%s"""
    return _fetch_one(query, (company_id, dealer_name))

def get_dealers(company_id, search=None):
    query = """SELECT dealer_id, dealer_name, contact_person, phone, email, gst_number, address, city, state, created_date FROM dealers WHERE company_id=%s"""

    params = [company_id]

    if search:
        query += """ AND (dealer_name LIKE %s OR contact_person LIKE %s OR email LIKE %s OR phone LIKE %s)"""
        like_search = f"%{search}%"

        params.extend([like_search, like_search, like_search, like_search])

    query += """ ORDER BY dealer_id ASC"""
    return _fetch_all(query, params)

def get_dealer_by_id(company_id, dealer_id):
    query = """SELECT dealer_id, dealer_name, contact_person, phone, email, gst_number, address, city, state, created_date FROM dealers WHERE company_id=%s AND dealer_id=%s"""
    return _fetch_one(query, (company_id, dealer_id))

def add_dealer(company_id, dealer_name, contact_person, phone, email, gst_number, address, city, state):
    if dealer_exists(company_id, dealer_name):
        return False

    query = """INSERT INTO dealers(company_id, dealer_name, contact_person, phone, email, gst_number, address, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    return _execute_commit(query, (company_id, dealer_name, contact_person, phone, email, gst_number, address, city, state), fetch_lastrow=True)

def update_dealer(dealer_id, company_id, dealer_name, contact_person, phone, email, gst_number, address, city, state
):
    query = """ UPDATE dealers
    SET dealer_name=%s, contact_person=%s, phone=%s, email=%s, gst_number=%s, address=%s, city=%s, state=%s
    WHERE dealer_id=%s AND company_id=%s
    """
    return _execute_commit(query, (dealer_name, contact_person, phone, email, gst_number, address, city, state, dealer_id, company_id))

def delete_dealer(dealer_id, company_id):
    query = """ DELETE FROM dealers WHERE dealer_id=%s AND company_id=%s"""
    return _execute_commit(query, (dealer_id, company_id))