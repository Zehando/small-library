# p1_overview.py

import streamlit as st
import pandas as pd
from sql_read_functions import get_all_members, get_all_books, get_all_loans_details, get_active_loans_details, get_available_books, search_books

st.title("📚 Liana's Library Overview")

st.markdown("---")

# --- Column Name Mappings for User-Friendly Display ---
MEMBER_COL_MAP = {
    'memberid': 'Member ID',
    'member_fname': 'First Name',
    'member_lname': 'Last Name',
    'signup_date': 'Signup Date',
    'address': 'Address',
    'mobile': 'Mobile Number',
    'email': 'Email Address',
    'social_media': 'Social Media',
    'preference': 'Communication Preference',
    'member_status': 'Status'
}

BOOK_COL_MAP = {
    'isbn': 'ISBN',
    'title': 'Title',
    'author_fname': 'Author First Name',
    'author_lname': 'Author Last Name',
    'publisher': 'Publisher',
    'publication_year': 'Publication Year',
    'genre': 'Genre'
}

# EXPANDED LOAN_COL_MAP to include joined table columns
LOAN_COL_MAP = {
    'loanid': 'Loan ID',
    'memberid': 'Member ID', # From Loans table
    'isbn': 'ISBN',           # From Loans table
    'borrow_date': 'Borrow Date',
    'return_date': 'Return Date',
    'member_fname': 'Member First Name', # From Members table (joined)
    'member_lname': 'Member Last Name',  # From Members table (joined)
    'email': 'Member Email',             # From Members table (joined)
    'title': 'Book Title',           # From Books table (joined)
    'author_fname': 'Book Author First Name', # From Books table (joined)
    'author_lname': 'Book Author Last Name'   # From Books table (joined)
}

# --- Function to display a dataframe with interactive controls ---
def display_data_with_controls(df, title, key_prefix, col_map):
    st.subheader(title)
    if not df.empty:
        # Apply renaming
        # Only rename columns that exist in the DataFrame
        df_display = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        max_rows = len(df_display)
        num_rows_to_show = st.slider(
            "Number of rows to display:",
            min_value=1,
            max_value=max_rows,
            value=min(10, max_rows), # Default to 10 rows or max available
            key=f"{key_prefix}_slider"
        )

        # Removed sorting options (sort_column and sort_order)
        # Removed email reminder button logic (manual table construction)

        # Apply row limit
        df_display = df_display.head(num_rows_to_show)

        # Display as a regular dataframe for all tables
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info(f"No {title.lower()} found.")

# Use tabs for different overview sections
tab_active_loans, tab_all_members, tab_all_books, tab_all_loan_history = st.tabs(
    ["📝 Active Loans", "👥 All Members", "📚 All Books", "📜 All Loan History"]
)

# --- Active Loans Tab ---
with tab_active_loans:
    active_loans_df = get_active_loans_details()
    display_data_with_controls(active_loans_df, "Current Active Loans", "active_loans", LOAN_COL_MAP)

# --- All Members Tab ---
with tab_all_members:
    members_df = get_all_members()
    display_data_with_controls(members_df, "All Library Members", "all_members", MEMBER_COL_MAP)

# --- All Books Tab ---
with tab_all_books:
    books_df = get_all_books()
    display_data_with_controls(books_df, "All Books in the Library", "all_books", BOOK_COL_MAP)

    st.markdown("---")

    # --- Conditional NEW SECTIONS: Available Books and Search Books (appear only within "All Books" tab) ---
    st.header("📖 Available Books")
    available_books_df = get_available_books()
    if not available_books_df.empty:
        st.dataframe(available_books_df.rename(columns={k: v for k, v in BOOK_COL_MAP.items() if k in available_books_df.columns}), use_container_width=True)
    else:
        st.info("No books currently available for loan.")

    st.markdown("---")

    st.header("🔍 Search Books by Title or Author")
    search_query_books_section = st.text_input("Enter book title or author to search:", key="book_search_input_overview")
    if search_query_books_section:
        searched_books_df = search_books(search_query_books_section)
        if not searched_books_df.empty:
            st.dataframe(searched_books_df.rename(columns={k: v for k, v in BOOK_COL_MAP.items() if k in searched_books_df.columns}), use_container_width=True)
        else:
            st.warning(f"No books found matching '{search_query_books_section}'.")
    else:
        st.info("Enter a search query to find books.")


# --- All Loan History Tab ---
with tab_all_loan_history:
    all_loans_df = get_all_loans_details()
    display_data_with_controls(all_loans_df, "All Loan History", "all_loans", LOAN_COL_MAP)

st.markdown("---")
st.markdown("Feel free to navigate to the 'Data Input' page to add or manage data!")
