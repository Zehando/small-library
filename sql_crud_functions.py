# sql_crud_functions.py

import pandas as pd
from sqlalchemy import text
from sql_con import engine
# IMPORTANT: get_available_books is now imported locally within add_loan()
# to prevent circular import issues. Do NOT uncomment the line below.
# from sql_read_functions import get_available_books

# --- Helper Functions ---

def _check_member_exists(member_id=None, email=None, mobile=None):
    """
    Checks if a member exists by ID, email, or mobile.
    Returns True if exists, False otherwise.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            if member_id:
                query = text("SELECT COUNT(*) FROM members WHERE memberid = :member_id;")
                result = connection.execute(query, {'member_id': member_id}).scalar()
                # print(f"DEBUG: _check_member_exists (ID={member_id}): Result count = {result}") # Debug line
                return result > 0
            if email:
                query = text("SELECT COUNT(*) FROM members WHERE email = :email;")
                result = connection.execute(query, {'email': email}).scalar()
                # print(f"DEBUG: _check_member_exists (Email={email}): Result count = {result}") # Debug line
                return result > 0
            if mobile:
                query = text("SELECT COUNT(*) FROM members WHERE mobile = :mobile;")
                result = connection.execute(query, {'mobile': mobile}).scalar()
                # print(f"DEBUG: _check_member_exists (Mobile={mobile}): Result count = {result}") # Debug line
                return result > 0
    except Exception as e:
        print(f"ERROR: _check_member_exists failed: {e}")
    return False

def _check_book_exists(isbn):
    """
    Checks if a book with the given ISBN exists.
    Returns True if exists, False otherwise.
    Adjusted for PostgreSQL's default lowercase table names.
    """
    try:
        with engine.connect() as connection:
            query = text("SELECT COUNT(*) FROM books WHERE isbn = :isbn;")
            result = connection.execute(query, {'isbn': isbn}).scalar()
            # print(f"DEBUG: _check_book_exists (ISBN={isbn}): Result count = {result}") # Debug line
            return result > 0
    except Exception as e:
        print(f"ERROR: _check_book_exists failed: {e}")
    return False

def _check_loan_exists(loan_id):
    """
    Checks if a loan with the given LoanID exists.
    Returns True if exists, False otherwise.
    Adjusted for PostgreSQL's default lowercase table names.
    """
    try:
        with engine.connect() as connection:
            query = text("SELECT COUNT(*) FROM loans WHERE loanid = :loan_id;")
            result = connection.execute(query, {'loan_id': loan_id}).scalar()
            # print(f"DEBUG: _check_loan_exists (LoanID={loan_id}): Result count = {result}") # Debug line
            return result > 0
    except Exception as e:
        print(f"ERROR: _check_loan_exists failed: {e}")
    return False

# --- Member CRUD Operations ---

def add_member(fname, lname, signup_date, address, mobile, email, social_media, preference, status):
    """
    Adds a new member to the members table.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if _check_member_exists(email=email):
            return False, "Error: Member with this email already exists."
        if _check_member_exists(mobile=mobile):
            return False, "Error: Member with this mobile number already exists."

        with engine.connect() as connection:
            query = text("""
                INSERT INTO members (member_fname, member_lname, signup_date, address, mobile, email, social_media, preference, member_status)
                VALUES (:fname, :lname, :signup_date, :address, :mobile, :email, :social_media, :preference, :status);
            """)
            connection.execute(query, {
                'fname': fname, 'lname': lname, 'signup_date': signup_date,
                'address': address, 'mobile': mobile, 'email': email,
                'social_media': social_media, 'preference': preference, 'status': status
            })
            connection.commit()
        return True, "Member added successfully!"
    except Exception as e:
        return False, f"Error adding member: {e}"

def get_member_details(member_id=None, email=None, mobile=None, fname=None, lname=None):
    """
    Retrieves a member's details by memberid, email, mobile, or first/last name.
    Prioritizes search: ID > Email > Mobile > FName+LName.
    Returns a DataFrame with member details or an empty DataFrame if not found.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query_str = "SELECT * FROM members WHERE 1=1"
            params = {}

            if member_id:
                query_str += " AND memberid = :member_id"
                params['member_id'] = member_id
            elif email:
                query_str += " AND email = :email"
                params['email'] = email
            elif mobile:
                query_str += " AND mobile = :mobile"
                params['mobile'] = mobile
            elif fname and lname:
                query_str += " AND member_fname = :fname AND member_lname = :lname"
                params['fname'] = fname
                params['lname'] = lname
            else:
                return pd.DataFrame() # No valid search criteria provided

            query = text(query_str)
            # print(f"DEBUG: Executing query for Member details: {query_str} with params {params}") # Debug line
            result_proxy = connection.execute(query, params)
            column_names = result_proxy.keys()
            result = result_proxy.fetchone()
            # print(f"DEBUG: Raw result for Member details: {result}") # Debug line
            if result:
                return pd.DataFrame([result], columns=column_names)
            return pd.DataFrame()
    except Exception as e:
        print(f"ERROR: get_member_details failed: {e}")
        return pd.DataFrame()


def update_member(member_id, fname, lname, signup_date, address, mobile, email, social_media, preference, status):
    """
    Updates an existing member's details.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_member_exists(member_id=member_id):
            return False, "Error: Member not found."

        # Check for duplicate email/mobile if they are being changed to an existing one (excluding self)
        with engine.connect() as connection:
            if email:
                check_email_query = text("SELECT memberid FROM members WHERE email = :email AND memberid != :member_id;")
                if connection.execute(check_email_query, {'email': email, 'member_id': member_id}).fetchone():
                    return False, "Error: Another member already uses this email."
            if mobile:
                check_mobile_query = text("SELECT memberid FROM members WHERE mobile = :mobile AND memberid != :member_id;")
                if connection.execute(check_mobile_query, {'mobile': mobile, 'member_id': member_id}).fetchone():
                    return False, "Error: Another member already uses this mobile number."

            query = text("""
                UPDATE members
                SET member_fname = :fname, member_lname = :lname, signup_date = :signup_date,
                    address = :address, mobile = :mobile, email = :email,
                    social_media = :social_media, preference = :preference, member_status = :status
                WHERE memberid = :member_id;
            """)
            connection.execute(query, {
                'member_id': member_id, 'fname': fname, 'lname': lname, 'signup_date': signup_date,
                'address': address, 'mobile': mobile, 'email': email,
                'social_media': social_media, 'preference': preference, 'status': status
            })
            connection.commit()
        return True, "Member updated successfully!"
    except Exception as e:
        return False, f"Error updating member: {e}"

def delete_member(member_id):
    """
    Deletes a member from the members table.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_member_exists(member_id=member_id):
            return False, "Error: Member not found."
        with engine.connect() as connection:
            # Check for active loans before deleting member
            check_loans_query = text("SELECT COUNT(*) FROM loans WHERE memberid = :member_id AND return_date IS NULL;")
            active_loans_count = connection.execute(check_loans_query, {'member_id': member_id}).scalar()
            if active_loans_count > 0:
                return False, f"Error: Member has {active_loans_count} active loan(s) and cannot be deleted."

            query = text("DELETE FROM members WHERE memberid = :member_id;")
            connection.execute(query, {'member_id': member_id})
            connection.commit()
        return True, "Member deleted successfully!"
    except Exception as e:
        return False, f"Error deleting member: {e}"

# --- Book CRUD Operations ---

def add_book(isbn, title, author_fname, author_lname, publisher, publication_year, genre):
    """
    Adds a new book or updates an existing one if ISBN matches.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if _check_book_exists(isbn):
            return False, "Error: Book with this ISBN already exists. Use update function if you want to modify it."
        with engine.connect() as connection:
            query = text("""
                INSERT INTO books (isbn, title, author_fname, author_lname, publisher, publication_year, genre)
                VALUES (:isbn, :title, :author_fname, :author_lname, :publisher, :publication_year, :genre);
            """)
            connection.execute(query, {
                'isbn': isbn, 'title': title, 'author_fname': author_fname,
                'author_lname': author_lname, 'publisher': publisher,
                'publication_year': publication_year, 'genre': genre
            })
            connection.commit()
        return True, "Book added successfully!"
    except Exception as e:
        return False, f"Error adding book: {e}"

def get_book_by_isbn(isbn):
    """
    Retrieves a book's details by ISBN.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM books WHERE isbn = :isbn;")
            # print(f"DEBUG: Executing query for ISBN: {isbn}") # Debug line
            result_proxy = connection.execute(query, {'isbn': isbn})
            column_names = result_proxy.keys() # Get column names from the Result object
            result = result_proxy.fetchone() # Fetch the row
            # print(f"DEBUG: Raw result for ISBN {isbn}: {result}") # Debug line
            if result:
                return pd.DataFrame([result], columns=column_names)
            return pd.DataFrame()
    except Exception as e:
        print(f"ERROR: get_book_by_isbn failed for ISBN {isbn}: {e}")
        return pd.DataFrame()

def update_book(isbn, title, author_fname, author_lname, publisher, publication_year, genre):
    """
    Updates an existing book's details.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_book_exists(isbn):
            return False, "Error: Book not found."
        with engine.connect() as connection:
            query = text("""
                UPDATE books
                SET title = :title, author_fname = :author_fname, author_lname = :author_lname,
                    publisher = :publisher, publication_year = :publication_year, genre = :genre
                WHERE isbn = :isbn;
            """)
            connection.execute(query, {
                'isbn': isbn, 'title': title, 'author_fname': author_fname,
                'author_lname': author_lname, 'publisher': publisher,
                'publication_year': publication_year, 'genre': genre
            })
            connection.commit()
        return True, "Book updated successfully!"
    except Exception as e:
        return False, f"Error updating book: {e}"

def delete_book(isbn):
    """
    Deletes a book from the books table.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_book_exists(isbn):
            return False, "Error: Book not found."
        with engine.connect() as connection:
            # Check for active loans before deleting book
            check_loans_query = text("SELECT COUNT(*) FROM loans WHERE isbn = :isbn AND return_date IS NULL;")
            active_loans_count = connection.execute(check_loans_query, {'isbn': isbn}).scalar()
            if active_loans_count > 0:
                return False, f"Error: Book has {active_loans_count} active loan(s) and cannot be deleted."

            query = text("DELETE FROM books WHERE isbn = :isbn;")
            connection.execute(query, {'isbn': isbn})
            connection.commit()
        return True, "Book deleted successfully!"
    except Exception as e:
        return False, f"Error deleting book: {e}"

# --- Loan CRUD Operations ---

def add_loan(member_id, isbn, borrow_date):
    """
    Adds a new loan, checking for book availability.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    # Import get_available_books locally to prevent circular import
    # This import MUST be inside the function if sql_read_functions eventually
    # imports anything from sql_crud_functions.
    from sql_read_functions import get_available_books

    try:
        # Check if member and book exist
        if not _check_member_exists(member_id=member_id):
            return False, "Error: Member not found."
        if not _check_book_exists(isbn):
            return False, "Error: Book not found."

        # Check if the book is available
        available_books_df = get_available_books()
        if isbn not in available_books_df['isbn'].values: # 'isbn' is the Python DataFrame column name, now lowercase
            return False, "Error: Book is currently not available for loan."

        with engine.connect() as connection:
            query = text("""
                INSERT INTO loans (memberid, isbn, borrow_date, return_date)
                VALUES (:member_id, :isbn, :borrow_date, NULL);
            """)
            connection.execute(query, {
                'member_id': member_id, 'isbn': isbn, 'borrow_date': borrow_date
            })
            connection.commit()
        return True, "Loan added successfully!"
    except Exception as e:
        return False, f"Error adding loan: {e}"

def get_loan_by_id(loan_id):
    """
    Retrieves a loan's details by loanid,
    including joined member and book information.
    Returns a DataFrame with loan, member, and book details or an empty DataFrame if not found.
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
                    B.author_fname AS book_author_fname, -- Renamed to avoid conflict if needed
                    B.author_lname AS book_author_lname -- Renamed to avoid conflict if needed
                FROM loans AS L
                JOIN members AS M ON L.memberid = M.memberid
                JOIN books AS B ON L.isbn = B.isbn
                WHERE L.loanid = :loan_id;
            """)
            # print(f"DEBUG: Executing query for LoanID: {loan_id}") # Debug line
            result_proxy = connection.execute(query, {'loan_id': loan_id})
            column_names = result_proxy.keys() # Get column names from the Result object
            result = result_proxy.fetchone() # Fetch the row
            # print(f"DEBUG: Raw result for LoanID {loan_id}: {result}") # Debug line
            if result:
                return pd.DataFrame([result], columns=column_names)
            return pd.DataFrame()
    except Exception as e:
        print(f"ERROR: get_loan_by_id failed for ID {loan_id}: {e}")
        return pd.DataFrame()

def update_loan_return_date(loan_id, return_date):
    """
    Updates the return date for an existing loan.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_loan_exists(loan_id):
            return False, "Error: Loan not found."
        with engine.connect() as connection:
            query = text("""
                UPDATE loans
                SET return_date = :return_date
                WHERE loanid = :loan_id;
            """)
            connection.execute(query, {'loan_id': loan_id, 'return_date': return_date})
            connection.commit()
        return True, "Loan return date updated successfully!"
    except Exception as e:
        return False, f"Error updating loan return date: {e}"

def delete_loan(loan_id):
    """
    Deletes a loan from the loans table.
    Adjusted for PostgreSQL's default lowercase table and column names.
    """
    try:
        if not _check_loan_exists(loan_id):
            return False, "Error: Loan not found."
        with engine.connect() as connection:
            query = text("DELETE FROM loans WHERE loanid = :loan_id;")
            connection.execute(query, {'loan_id': loan_id})
            connection.commit()
        return True, "Loan deleted successfully!"
    except Exception as e:
        return False, f"Error deleting loan: {e}"

# --- Bulk Upload Functions ---

def bulk_insert_members_from_df(df):
    """
    Inserts multiple members from a DataFrame.
    Adjusted to handle potential case differences from CSV headers
    and map to PostgreSQL's lowercase column names.
    """
    results = []
    # Map DataFrame column names to expected database column names (lowercase)
    df_mapped = df.rename(columns={
        'Member_FName': 'member_fname', 'Member_LName': 'member_lname',
        'Signup_Date': 'signup_date', 'Address': 'address', 'Mobile': 'mobile',
        'Email': 'email', 'Social_Media': 'social_media', 'Preference': 'preference',
        'Member_Status': 'member_status', 'MemberID': 'memberid' # Include MemberID if present in CSV
    })

    for index, row in df_mapped.iterrows():
        # Ensure all required fields are present and not NaN/None
        required_fields = ['member_fname', 'member_lname', 'signup_date', 'address', 'mobile', 'email', 'preference', 'member_status']
        if not all(pd.notna(row.get(field)) for field in required_fields):
            results.append(f"Row {index + 1}: Skipping due to missing required data.")
            continue

        # If MemberID is provided in the CSV, include it in the insert.
        # Otherwise, let SERIAL generate it.
        member_id_val = row.get('memberid') if pd.notna(row.get('memberid')) else None

        try:
            with engine.connect() as connection:
                if member_id_val is not None:
                    # Insert with explicit MemberID
                    query = text("""
                        INSERT INTO members (memberid, member_fname, member_lname, signup_date, address, mobile, email, social_media, preference, member_status)
                        VALUES (:memberid, :fname, :lname, :signup_date, :address, :mobile, :email, :social_media, :preference, :status);
                    """)
                    connection.execute(query, {
                        'memberid': member_id_val,
                        'fname': row.get('member_fname'), 'lname': row.get('member_lname'), 'signup_date': row.get('signup_date'),
                        'address': row.get('address'), 'mobile': row.get('mobile'), 'email': row.get('email'),
                        'social_media': row.get('social_media', ''),
                        'preference': row.get('preference'), 'status': row.get('member_status')
                    })
                else:
                    # Insert without MemberID, let SERIAL handle it
                    query = text("""
                        INSERT INTO members (member_fname, member_lname, signup_date, address, mobile, email, social_media, preference, member_status)
                        VALUES (:fname, :lname, :signup_date, :address, :mobile, :email, :social_media, :preference, :status);
                    """)
                    connection.execute(query, {
                        'fname': row.get('member_fname'), 'lname': row.get('member_lname'), 'signup_date': row.get('signup_date'),
                        'address': row.get('address'), 'mobile': row.get('mobile'), 'email': row.get('email'),
                        'social_media': row.get('social_media', ''),
                        'preference': row.get('preference'), 'status': row.get('member_status')
                    })
                connection.commit()
            results.append(f"Row {index + 1}: Member added successfully!")
        except Exception as e:
            results.append(f"Row {index + 1}: Error adding member: {e}")
    return results


def bulk_insert_books_from_df(df):
    """
    Inserts multiple books from a DataFrame.
    Adjusted to handle potential case differences from CSV headers
    and map to PostgreSQL's lowercase column names.
    """
    results = []
    df_mapped = df.rename(columns={
        'ISBN': 'isbn', 'Title': 'title', 'Author_FName': 'author_fname',
        'Author_LName': 'author_lname', 'Publisher': 'publisher',
        'Publication_Year': 'publication_year', 'Genre': 'genre'
    })

    for index, row in df_mapped.iterrows():
        required_fields = ['isbn', 'title', 'author_fname', 'author_lname', 'publisher', 'publication_year', 'genre']
        if not all(pd.notna(row.get(field)) for field in required_fields):
            results.append(f"Row {index + 1}: Skipping due to missing required data.")
            continue

        success, message = add_book(
            isbn=row.get('isbn'),
            title=row.get('title'),
            author_fname=row.get('author_fname'),
            author_lname=row.get('author_lname'),
            publisher=row.get('publisher'),
            publication_year=row.get('publication_year'),
            genre=row.get('genre')
        )
        results.append(f"Row {index + 1}: {message}")
    return results

def bulk_insert_loans_from_df(df):
    """
    Inserts multiple loans from a DataFrame.
    Adjusted to handle potential case differences from CSV headers
    and map to PostgreSQL's lowercase column names.
    """
    results = []
    df_mapped = df.rename(columns={
        'LoanID': 'loanid', 'MemberID': 'memberid', 'ISBN': 'isbn',
        'Borrow_date': 'borrow_date', 'Return_date': 'return_date'
    })

    for index, row in df_mapped.iterrows():
        required_fields = ['memberid', 'isbn', 'borrow_date']
        if not all(pd.notna(row.get(field)) for field in required_fields):
            results.append(f"Row {index + 1}: Skipping due to missing required data.")
            continue

        # If LoanID is provided in the CSV, include it in the insert.
        # Otherwise, let SERIAL generate it.
        loan_id_val = row.get('loanid') if pd.notna(row.get('loanid')) else None
        return_date_val = row.get('return_date') if pd.notna(row.get('return_date')) else None

        try:
            with engine.connect() as connection:
                if loan_id_val is not None:
                    # Insert with explicit LoanID
                    query = text("""
                        INSERT INTO loans (loanid, memberid, isbn, borrow_date, return_date)
                        VALUES (:loanid, :member_id, :isbn, :borrow_date, :return_date);
                    """)
                    connection.execute(query, {
                        'loanid': loan_id_val,
                        'member_id': row.get('memberid'), 'isbn': row.get('isbn'),
                        'borrow_date': row.get('borrow_date'), 'return_date': return_date_val
                    })
                else:
                    # Insert without LoanID, let SERIAL handle it
                    query = text("""
                        INSERT INTO loans (memberid, isbn, borrow_date, return_date)
                        VALUES (:member_id, :isbn, :borrow_date, :return_date);
                    """)
                    connection.execute(query, {
                        'member_id': row.get('memberid'), 'isbn': row.get('isbn'),
                        'borrow_date': row.get('borrow_date'), 'return_date': return_date_val
                    })
                connection.commit()
            results.append(f"Row {index + 1}: Loan added successfully!")
        except Exception as e:
            results.append(f"Row {index + 1}: Error adding loan: {e}")
    return results
