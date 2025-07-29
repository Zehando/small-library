# sql_read_functions.py

import pandas as pd
from sqlalchemy import text
from sql_con import get_engine # Use get_engine function
import streamlit as st # Import streamlit to use st.error for database connection issues

# --- Helper function for executing queries and returning DataFrame ---
def _execute_query_to_dataframe(query_str, params=None):
    engine = get_engine()
    if engine is None:
        st.error("Database connection not established. Please check sql_con.py and your secrets.")
        return pd.DataFrame()
    try:
        with engine.connect() as connection:
            result_proxy = connection.execute(text(query_str), params if params else {})
            column_names = result_proxy.keys()
            data = result_proxy.fetchall()
            return pd.DataFrame(data, columns=column_names)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

# --- Read Functions ---

def get_all_members():
    """Retrieves all members from the members table."""
    query = "SELECT * FROM members;"
    return _execute_query_to_dataframe(query)

def get_all_books():
    """Retrieves all books from the books table."""
    query = "SELECT * FROM books;"
    return _execute_query_to_dataframe(query)

def get_all_loans():
    """
    Retrieves all loans with associated member and book details.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    query = """
    SELECT
        L.loanid,
        L.memberid,
        M.member_fname,
        M.member_lname,
        L.isbn,
        B.title,
        B.author_fname,
        B.author_lname,
        L.borrow_date,
        L.return_date
    FROM loans AS L
    JOIN members AS M ON L.memberid = M.memberid
    JOIN books AS B ON L.isbn = B.isbn
    ORDER BY L.loanid DESC;
    """
    return _execute_query_to_dataframe(query)

def get_active_loans_details():
    """
    Retrieves details of all active loans (where return_date is NULL)
    including member and book information.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    query = """
    SELECT
        L.loanid,
        L.memberid,
        M.member_fname,
        M.member_lname,
        L.isbn,
        B.title,
        B.author_fname,
        B.author_lname,
        L.borrow_date,
        L.return_date
    FROM loans AS L
    JOIN members AS M ON L.memberid = M.memberid
    JOIN books AS B ON L.isbn = B.isbn
    WHERE L.return_date IS NULL
    ORDER BY L.borrow_date ASC;
    """
    return _execute_query_to_dataframe(query)

def search_books(search_term):
    """
    Searches for books by title or author (first or last name).
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    search_term_lower = f"%{search_term.lower()}%" # Case-insensitive search
    query = """
    SELECT * FROM books
    WHERE LOWER(title) LIKE :search_term
    OR LOWER(author_fname) LIKE :search_term
    OR LOWER(author_lname) LIKE :search_term;
    """
    return _execute_query_to_dataframe(query, {'search_term': search_term_lower})

def get_available_books():
    """
    Retrieves books that are currently available for loan.
    A book is available if it's not currently associated with an active loan (return_date IS NULL).
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    query = """
    SELECT B.*
    FROM books AS B
    LEFT JOIN loans AS L ON B.isbn = L.isbn AND L.return_date IS NULL
    WHERE L.loanid IS NULL;
    """
    return _execute_query_to_dataframe(query)
