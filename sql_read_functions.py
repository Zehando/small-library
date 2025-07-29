# sql_read_functions.py

import pandas as pd
from sqlalchemy import text
from sql_con import engine # Assuming sql_con.py provides the SQLAlchemy engine

# Function to fetch all members from the Members table
def get_all_members():
    """
    Fetches all records from the members table and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table names.
    """
    try:
        with engine.connect() as connection:
            # Execute a SQL query to select all data from the members table (lowercase)
            result = connection.execute(text("SELECT * FROM members;"))
            # Fetch all rows from the result
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching members: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Function to fetch all books from the Books table
def get_all_books():
    """
    Fetches all records from the books table and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table names.
    """
    try:
        with engine.connect() as connection:
            # Execute a SQL query to select all data from the books table (lowercase)
            result = connection.execute(text("SELECT * FROM books;"))
            # Fetch all rows from the result
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching books: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Function to fetch all loans from the Loans table
def get_all_loans():
    """
    Fetches all records from the loans table and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table names.
    """
    try:
        with engine.connect() as connection:
            # Execute a SQL query to select all data from the loans table (lowercase)
            result = connection.execute(text("SELECT * FROM loans;"))
            # Fetch all rows from the result
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching loans: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Function to get active loans with book and member details
def get_active_loans_details():
    """
    Fetches details of active loans (where return_date is NULL)
    including member and book information, and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT
                    L.loanid,
                    M.member_fname,
                    M.member_lname,
                    B.title,
                    B.author_fname,
                    B.author_lname,
                    L.borrow_date,
                    M.email -- Added email for consistency with p2_datainput loan email reminder
                FROM
                    loans AS L
                JOIN
                    members AS M ON L.memberid = M.memberid
                JOIN
                    books AS B ON L.isbn = B.isbn
                WHERE
                    L.return_date IS NULL;
            """)
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching active loan details: {e}")
        return pd.DataFrame()

# Function to get all loans with book and member details
def get_all_loans_details():
    """
    Fetches details of all loans including member and book information,
    and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT
                    L.loanid,
                    M.member_fname,
                    M.member_lname,
                    B.title,
                    B.author_fname,
                    B.author_lname,
                    L.borrow_date,
                    L.return_date,
                    M.email -- Added email for consistency with p2_datainput loan email reminder
                FROM
                    loans AS L
                JOIN
                    members AS M ON L.memberid = M.memberid
                JOIN
                    books AS B ON L.isbn = B.isbn;
            """)
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching all loan details: {e}")
        return pd.DataFrame()

# NEW FUNCTION: Get available books (not currently on loan)
def get_available_books():
    """
    Fetches books that are not currently on loan (i.e., not present in the loans table
    with a NULL return_date) and returns them as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT
                    B.isbn,
                    B.title,
                    B.author_fname,
                    B.author_lname,
                    B.publisher,
                    B.publication_year,
                    B.genre
                FROM
                    books AS B
                LEFT JOIN
                    loans AS L ON B.isbn = L.isbn AND L.return_date IS NULL
                WHERE
                    L.isbn IS NULL;
            """)
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching available books: {e}")
        return pd.DataFrame()

# NEW FUNCTION: Search books by title or author
def search_books(query_text):
    """
    Searches for books by matching the query_text against title, author_fname, or author_lname.
    Returns matching books as a Pandas DataFrame.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            # Using LIKE for partial matches and parameters to prevent SQL injection
            sql_query = text(f"""
                SELECT
                    isbn,
                    title,
                    author_fname,
                    author_lname,
                    publisher,
                    publication_year,
                    genre
                FROM
                    books
                WHERE
                    title LIKE :query OR
                    author_fname LIKE :query OR
                    author_lname LIKE :query;
            """)
            # Add wildcards to the query text for LIKE operator
            params = {'query': f"%{query_text}%"}
            result = connection.execute(sql_query, params)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error searching books: {e}")
        return pd.DataFrame()

# NEW FUNCTION: Get active loans for dropdown selection
def get_active_loans_for_dropdown():
    """
    Fetches active loans with member and book details formatted for dropdown selection.
    Returns a DataFrame with loan details for UI dropdown.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT
                    L.loanid,
                    L.memberid,
                    L.isbn,
                    L.borrow_date,
                    L.return_date,
                    M.member_fname,
                    M.member_lname,
                    M.email,
                    B.title,
                    B.author_fname,
                    B.author_lname
                FROM
                    loans AS L
                JOIN
                    members AS M ON L.memberid = M.memberid
                JOIN
                    books AS B ON L.isbn = B.isbn
                WHERE
                    L.return_date IS NULL
                ORDER BY L.borrow_date DESC;
            """)
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        print(f"Error fetching active loans for dropdown: {e}")
        return pd.DataFrame()
