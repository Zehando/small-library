# p2_datainput.py

import streamlit as st
import pandas as pd
from datetime import date
from sql_crud_functions import (
    add_member, get_member_details, update_member, delete_member,
    add_book, get_book_by_isbn, update_book, delete_book,
    add_loan, get_loan_by_id, update_loan_return_date, delete_loan,
    bulk_insert_members_from_df, bulk_insert_books_from_df, bulk_insert_loans_from_df
)
from sql_read_functions import get_all_members, get_all_books, get_all_loans # Ensure get_all_loans is imported
import urllib.parse # For URL encoding email body

def run(): # All Streamlit UI code MUST be inside this function for st.Page navigation
    st.title("➕ Data Input & Management")
    st.markdown("---")

    # Initialize session state for update forms if not already present
    if 'member_update_data' not in st.session_state:
        st.session_state.member_update_data = {}
    if 'book_update_data' not in st.session_state:
        st.session_state.book_update_data = {}
    if 'loan_update_data' not in st.session_state:
        st.session_state.loan_update_data = {}


    # Use tabs for different sections (Members, Books, Loans)
    tab_members, tab_books, tab_loans = st.tabs(["👥 Members", "📚 Books", "📝 Loans"])

    # --- Members Tab ---
    with tab_members:
        st.header("👥 Manage Members")

        # Add Member Section
        st.subheader("Add New Member")
        with st.form("add_member_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                member_fname = st.text_input("First Name*", max_chars=100, key="add_mem_fname")
                member_lname = st.text_input("Last Name*", max_chars=100, key="add_mem_lname")
                member_email = st.text_input("Email*", max_chars=100, key="add_mem_email")
                member_mobile = st.text_input("Mobile*", max_chars=20, key="add_mem_mobile")
            with col2:
                member_address = st.text_area("Address*", max_chars=255, key="add_mem_address")
                member_signup_date = st.date_input("Signup Date*", value="today", key="add_mem_signup_date")
                member_social_media = st.text_input("Social Media (Optional)", max_chars=255, key="add_mem_social_media")
                member_preference = st.selectbox("Communication Preference*", ['Email', 'Mobile', 'Address', 'Social Media'], key="add_mem_preference")
                member_status = st.selectbox("Member Status*", ['active', 'inactive', 'suspended'], key="add_mem_status")

            add_member_submit = st.form_submit_button("Add Member")

            if add_member_submit:
                if not all([member_fname, member_lname, member_email, member_mobile, member_address, member_signup_date]):
                    st.error("Please fill in all required fields (marked with *).")
                else:
                    success, message = add_member(
                        member_fname, member_lname, member_signup_date, member_address,
                        member_mobile, member_email, member_social_media, member_preference, member_status
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown("---")

        # Update Member Section - Retrieval Part
        st.subheader("Update Member Details")
        with st.form("retrieve_member_form", clear_on_submit=True): # Separate form for retrieval
            st.markdown("Enter **ONE** of the following to retrieve member data:")
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                member_id_to_retrieve = st.number_input("Member ID:", min_value=0, format="%d", key="retrieve_member_id_input")
                member_email_to_retrieve = st.text_input("Email Address:", key="retrieve_member_email_input")
            with col_search2:
                member_mobile_to_retrieve = st.text_input("Mobile Number:", key="retrieve_member_mobile_input")
                col_name1, col_name2 = st.columns(2)
                with col_name1:
                    member_fname_to_retrieve = st.text_input("First Name:", key="retrieve_member_fname_input")
                with col_name2:
                    member_lname_to_retrieve = st.text_input("Last Name:", key="retrieve_member_lname_input")

            retrieve_member_button = st.form_submit_button("Retrieve Member Data")

            if retrieve_member_button:
                retrieved_df = pd.DataFrame()
                search_performed = False

                if member_id_to_retrieve > 0:
                    retrieved_df = get_member_details(member_id=member_id_to_retrieve)
                    search_performed = True
                elif member_email_to_retrieve.strip():
                    retrieved_df = get_member_details(email=member_email_to_retrieve.strip())
                    search_performed = True
                elif member_mobile_to_retrieve.strip():
                    retrieved_df = get_member_details(mobile=member_mobile_to_retrieve.strip())
                    search_performed = True
                elif member_fname_to_retrieve.strip() and member_lname_to_retrieve.strip():
                    retrieved_df = get_member_details(fname=member_fname_to_retrieve.strip(), lname=member_lname_to_retrieve.strip())
                    search_performed = True
                else:
                    st.warning("Please provide a Member ID, Email, Mobile, or both First and Last Name to retrieve data.")

                if search_performed:
                    if not retrieved_df.empty:
                        # Store data with lowercase keys as returned by PostgreSQL
                        st.session_state.member_update_data = retrieved_df.iloc[0].to_dict()
                        st.success(f"Data for Member ID {st.session_state.member_update_data.get('memberid')} retrieved. You can now modify the fields below.")
                    else:
                        st.session_state.member_update_data = {} # Clear previous data if not found
                        st.warning("Member data not found for the provided criteria.")
                else:
                    st.session_state.member_update_data = {} # Clear if no search performed


        # Update Member Section - Modification Part (only shown if data is retrieved)
        if st.session_state.member_update_data:
            st.markdown("---") # Separator for clarity
            st.subheader("Modify Member Data")
            with st.form("modify_member_form", clear_on_submit=False): # Separate form for modification
                member_data = st.session_state.member_update_data # Get current session state data

                # Debugging: Print what's in member_data right before populating fields
                # st.write("DEBUG: member_data for population:", member_data)
                # st.write("DEBUG: Keys in member_data for population:", member_data.keys())

                # Populate fields from session state using lowercase keys
                upd_fname = st.text_input("First Name", value=member_data.get('member_fname', ''), key="upd_fname_mod")
                upd_lname = st.text_input("Last Name", value=member_data.get('member_lname', ''), key="upd_lname_mod")
                upd_email = st.text_input("Email", value=member_data.get('email', ''), key="upd_email_mod")
                upd_mobile = st.text_input("Mobile", value=member_data.get('mobile', ''), key="upd_mobile_mod")
                upd_address = st.text_area("Address", value=member_data.get('address', ''), key="upd_address_mod")

                # Handle date_input value for potential NaT or None
                signup_date_value = date.today()
                if 'signup_date' in member_data and pd.notna(member_data['signup_date']):
                    try:
                        signup_date_value = pd.to_datetime(member_data['signup_date']).date()
                    except ValueError:
                        pass # Keep default if conversion fails

                upd_signup_date = st.date_input("Signup Date", value=signup_date_value, key="upd_signup_date_mod")

                upd_social_media = st.text_input("Social Media", value=member_data.get('social_media', ''), key="upd_social_media_mod")

                upd_preference_options = ['Email', 'Mobile', 'Address', 'Social Media']
                # Use lowercase key for lookup
                upd_preference_index = upd_preference_options.index(member_data['preference']) if 'preference' in member_data and member_data['preference'] in upd_preference_options else 0
                upd_preference = st.selectbox("Communication Preference", upd_preference_options, index=upd_preference_index, key="upd_preference_mod")

                upd_status_options = ['active', 'inactive', 'suspended']
                # Use lowercase key for lookup
                upd_status_index = upd_status_options.index(member_data['member_status']) if 'member_status' in member_data and member_data['member_status'] in upd_status_options else 0
                upd_status = st.selectbox("Member Status", upd_status_options, index=upd_status_index, key="upd_status_mod")


                update_member_submit = st.form_submit_button("Update Member")

                if update_member_submit:
                    # Get the MemberID from the retrieved data for the update operation (lowercase key)
                    member_id_for_update = st.session_state.member_update_data.get('memberid')

                    if not member_id_for_update: # Should not happen if form is shown, but as a safeguard
                        st.error("Internal Error: Member ID not found for update. Please re-retrieve data.")
                    elif not (upd_fname.strip() and upd_lname.strip() and upd_email.strip() and upd_mobile.strip() and upd_address.strip() and upd_signup_date):
                        st.error("Please ensure all required fields are filled for update.")
                    else:
                        success, message = update_member(
                            member_id_for_update, upd_fname, upd_lname, upd_signup_date, upd_address,
                            upd_mobile, upd_email, upd_social_media, upd_preference, upd_status
                        )
                        if success:
                            st.success(message)
                            st.session_state.member_update_data = {} # Clear form after successful update
                            st.rerun() # Rerun to hide the modification form and clear inputs
                        else:
                            st.error(message)

        st.markdown("---")

        # Delete Member Section
        st.subheader("Delete Member")
        with st.form("delete_member_form", clear_on_submit=True):
            member_id_to_delete = st.number_input("Enter Member ID to Delete:", min_value=1, format="%d", key="delete_member_id_input")
            delete_member_submit = st.form_submit_button("Delete Member")
            if delete_member_submit and member_id_to_delete:
                success, message = delete_member(member_id_to_delete)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        st.markdown("---")

        # Bulk Upload Members
        st.subheader("Bulk Upload Members (CSV)")
        uploaded_members_file = st.file_uploader("Upload CSV file for Members", type=["csv"], key="upload_members_csv")
        if uploaded_members_file:
            try:
                members_df_upload = pd.read_csv(uploaded_members_file)
                st.write("Preview of uploaded data:")
                st.dataframe(members_df_upload.head())
                if st.button("Process Bulk Member Upload", key="process_bulk_members"):
                    results = bulk_insert_members_from_df(members_df_upload)
                    for res in results:
                        if "Error" in res:
                            st.error(res)
                        else:
                            st.success(res)
                    st.success("Bulk member upload process completed.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")


    # --- Books Tab ---
    with tab_books:
        st.header("📚 Manage Books")

        # Add Book Section
        st.subheader("Add New Book")
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                book_isbn = st.text_input("ISBN*", max_chars=20, key="add_book_isbn")
                book_title = st.text_input("Title*", max_chars=255, key="add_book_title")
                book_author_fname = st.text_input("Author First Name*", max_chars=255, key="add_book_author_fname")
                book_author_lname = st.text_input("Author Last Name*", max_chars=255, key="add_book_author_lname")
            with col2:
                book_publisher = st.text_input("Publisher*", max_chars=255, key="add_book_publisher")
                book_publication_year = st.number_input("Publication Year (YYYY)*", min_value=1000, max_value=date.today().year + 5, format="%d", key="add_book_pub_year") # Allow future years for upcoming books
                book_genre = st.text_input("Genre*", max_chars=50, key="add_book_genre")

            add_book_submit = st.form_submit_button("Add Book")

            if add_book_submit:
                if not all([book_isbn, book_title, book_author_fname, book_author_lname, book_publisher, book_publication_year, book_genre]):
                    st.error("Please fill in all required fields (marked with *).")
                else:
                    success, message = add_book(
                        book_isbn, book_title, book_author_fname, book_author_lname,
                        book_publisher, book_publication_year, book_genre
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown("---")

        # Update Book Section
        st.subheader("Update Book Details")
        with st.form("update_book_form", clear_on_submit=False):
            isbn_to_update = st.text_input("Enter ISBN to Update:", key="update_isbn_input_form")
            retrieve_book_button = st.form_submit_button("Retrieve Book Data")

            if retrieve_book_button and isbn_to_update:
                book_df = get_book_by_isbn(isbn_to_update)
                if not book_df.empty:
                    # Store data with lowercase keys
                    st.session_state.book_update_data = book_df.iloc[0].to_dict()
                    st.success(f"Data for ISBN {isbn_to_update} retrieved. You can now modify the fields below.")
                else:
                    st.session_state.book_update_data = {} # Clear previous data if ISBN not found
                    st.warning("Book ISBN not found.")

            # Populate fields from session state using lowercase keys
            book_data = st.session_state.book_update_data

            update_book_col1, update_book_col2 = st.columns(2)
            with update_book_col1:
                upd_book_title = st.text_input("Title", value=book_data.get('title', ''), key="upd_book_title")
                upd_book_author_fname = st.text_input("Author First Name", value=book_data.get('author_fname', ''), key="upd_book_author_fname")
                upd_book_author_lname = st.text_input("Author Last Name", value=book_data.get('author_lname', ''), key="upd_book_author_lname")
            with update_book_col2:
                upd_book_publisher = st.text_input("Publisher", value=book_data.get('publisher', ''), key="upd_book_publisher")
                upd_book_publication_year = st.number_input(
                    "Publication Year (YYYY)",
                    min_value=1000,
                    max_value=date.today().year + 5,
                    value=book_data.get('publication_year', date.today().year), # Use lowercase key
                    format="%d",
                    key="upd_book_publication_year"
                )
                upd_book_genre = st.text_input("Genre", value=book_data.get('genre', ''), key="upd_book_genre")

            update_book_submit = st.form_submit_button("Update Book")

            if update_book_submit and isbn_to_update:
                if not book_data: # Check if data was actually retrieved
                    st.error("Please retrieve book data first by entering an ISBN and clicking 'Retrieve Book Data'.")
                # Refined validation check for book update
                elif not (upd_book_title.strip() and upd_book_author_fname.strip() and upd_book_author_lname.strip() and upd_book_publisher.strip() and upd_book_publication_year and upd_book_genre.strip()):
                    st.error("Please ensure all required fields are filled for update.")
                else:
                    success, message = update_book(
                        isbn_to_update, upd_book_title, upd_book_author_fname, upd_book_author_lname,
                        upd_book_publisher, upd_book_publication_year, upd_book_genre
                    )
                    if success:
                        st.success(message)
                        st.session_state.book_update_data = {} # Clear form after successful update
                    else:
                        st.error(message)

        st.markdown("---")

        # Delete Book Section
        st.subheader("Delete Book")
        with st.form("delete_book_form", clear_on_submit=True):
            isbn_to_delete = st.text_input("Enter ISBN to Delete:", key="delete_isbn_input")
            delete_book_submit = st.form_submit_button("Delete Book")
            if delete_book_submit and isbn_to_delete:
                success, message = delete_book(isbn_to_delete)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        st.markdown("---")

        # Bulk Upload Books
        st.subheader("Bulk Upload Books (CSV)")
        uploaded_books_file = st.file_uploader("Upload CSV file for Books", type=["csv"], key="upload_books_csv")
        if uploaded_books_file:
            try:
                books_df_upload = pd.read_csv(uploaded_books_file)
                st.write("Preview of uploaded data:")
                st.dataframe(books_df_upload.head())
                if st.button("Process Bulk Book Upload", key="process_bulk_books"):
                    results = bulk_insert_books_from_df(books_df_upload)
                    for res in results:
                        if "Error" in res:
                            st.error(res)
                        else:
                            st.success(res)
                    st.success("Bulk book upload process completed.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")


    # --- Loans Tab ---
    with tab_loans:
        st.header("📝 Manage Loans")

        # Add Loan Section
        st.subheader("Add New Loan")
        # Fetch members and books for dropdowns
        all_members_df = get_all_members()
        all_books_df = get_all_books()

        # Adjusting column names to lowercase for DataFrame access
        member_options = {f"{row['member_fname']} {row['member_lname']} (ID: {row['memberid']})": row['memberid'] for index, row in all_members_df.iterrows()}
        book_options = {f"{row['title']} by {row['author_lname']} (ISBN: {row['isbn']})": row['isbn'] for index, row in all_books_df.iterrows()}

        with st.form("add_loan_form", clear_on_submit=True):
            # Handle case where no members or books are available
            if not member_options:
                st.warning("No members available. Please add members first.")
                selected_member_display = None
            else:
                selected_member_display = st.selectbox("Select Member:", list(member_options.keys()), key="loan_member_select")

            if not book_options:
                st.warning("No books available. Please add books first.")
                selected_book_display = None
            else:
                selected_book_display = st.selectbox("Select Book:", list(book_options.keys()), key="loan_book_select")

            borrow_date = st.date_input("Borrow Date:", value="today", key="loan_borrow_date")

            add_loan_submit = st.form_submit_button("Add Loan")

            if add_loan_submit:
                if selected_member_display and selected_book_display and borrow_date:
                    member_id = member_options[selected_member_display]
                    isbn = book_options[selected_book_display]

                    success, message = add_loan(member_id, isbn, borrow_date)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please ensure a member and a book are selected, and a borrow date is provided.")

        st.markdown("---")

        # Update/Delete Loan Section (combined and modified)
        st.subheader("Update/Delete Loan")

        # 1. Fetch all loans for dropdown
        all_loans_for_update_df = get_all_loans()

        # 2. Create dropdown for loan selection
        loan_display_options = {}
        if not all_loans_for_update_df.empty:
            for index, row in all_loans_for_update_df.iterrows():
                # Ensure column names are lowercase as returned by PostgreSQL
                # Safely get date strings, handling NaT for return_date
                borrow_date_str = row['borrow_date'].strftime('%Y-%m-%d') if pd.notna(row['borrow_date']) else 'N/A'
                return_date_str = row['return_date'].strftime('%Y-%m-%d') if pd.notna(row['return_date']) else 'N/A'

                display_string = (
                    f"ID: {row['loanid']} | Member: {row['member_fname']} {row['member_lname']} | Book: {row['title']} "
                    f"| Borrow: {borrow_date_str} "
                    f"| Return: {return_date_str}"
                )
                loan_display_options[display_string] = row['loanid']

        selected_loan_display = st.selectbox(
            "Select Loan to Update/Delete:",
            list(loan_display_options.keys()),
            index=0 if loan_display_options else None,
            key="select_loan_to_update"
        )

        # If a loan is selected, retrieve its full details and populate session state
        if selected_loan_display:
            selected_loan_id = loan_display_options[selected_loan_display]
            loan_df_for_update = get_loan_by_id(selected_loan_id)
            if not loan_df_for_update.empty:
                st.session_state.loan_update_data = loan_df_for_update.iloc[0].to_dict()
                st.info(f"Details for Loan ID {selected_loan_id} loaded. Use the form below to modify or delete.")
            else:
                st.session_state.loan_update_data = {}
                st.warning("Selected loan details not found.")
        else:
            st.session_state.loan_update_data = {} # Clear if no loan selected

        # Only show the update/delete form if loan data is available in session state
        if st.session_state.loan_update_data:
            loan_data = st.session_state.loan_update_data

            with st.form("update_delete_loan_form", clear_on_submit=False):
                st.write(f"**Selected Loan ID:** {loan_data.get('loanid')}")
                # Accessing member and book details from the joined loan_data
                st.write(f"**Member:** {loan_data.get('member_fname', '')} {loan_data.get('member_lname', '')} (ID: {loan_data.get('memberid')})")
                st.write(f"**Book:** {loan_data.get('title', '')} by {loan_data.get('book_author_fname', '')} {loan_data.get('book_author_lname', '')} (ISBN: {loan_data.get('isbn')})")
                st.write(f"**Borrow Date:** {loan_data.get('borrow_date').strftime('%Y-%m-%d') if pd.notna(loan_data.get('borrow_date')) else 'N/A'}")
                st.write(f"**Current Return Date:** {loan_data.get('return_date').strftime('%Y-%m-%d') if pd.notna(loan_data.get('return_date')) else 'Not Returned Yet'}")

                # Date input for return date
                upd_return_date = st.date_input(
                    "Set Return Date:",
                    value=pd.to_datetime(loan_data['return_date']).date() if 'return_date' in loan_data and pd.notna(loan_data['return_date']) else date.today(),
                    key="upd_loan_return_date_mod"
                )

                col_buttons = st.columns(2)
                with col_buttons[0]:
                    update_loan_submit = st.form_submit_button("Update Loan Return Date")
                with col_buttons[1]:
                    delete_loan_confirm_button = st.form_submit_button("Delete Loan", help="Click to confirm deletion")

                if update_loan_submit:
                    if upd_return_date:
                        success, message = update_loan_return_date(loan_data['loanid'], upd_return_date)
                        if success:
                            st.success(message)
                            st.session_state.loan_update_data = {} # Clear form
                            st.rerun() # Rerun to refresh the dropdown and hide form
                        else:
                            st.error(message)
                    else:
                        st.error("Please provide a return date.")

                if delete_loan_confirm_button:
                    # Direct delete (Streamlit doesn't have native confirm dialog in sandbox)
                    success, message = delete_loan(loan_data['loanid'])
                    if success:
                        st.success(message)
                        st.session_state.loan_update_data = {} # Clear form
                        st.rerun() # Rerun to refresh the dropdown and hide form
                    else:
                        st.error(message)

                # Email Reminder Button (remains the same)
                if loan_data and loan_data.get('email'):
                    member_name = f"{loan_data.get('member_fname', '')} {loan_data.get('member_lname', '')}".strip()
                    member_email = loan_data.get('email', '')
                    book_title = loan_data.get('title', '')
                    borrow_date_str = loan_data.get('borrow_date', 'N/A').strftime('%Y-%m-%d') if pd.notna(loan_data.get('borrow_date')) else 'N/A'
                    loan_id = loan_data.get('loanid', 'N/A')

                    email_subject = urllib.parse.quote(f"Library Loan Reminder: '{book_title}' (Loan ID: {loan_id})")
                    email_body = urllib.parse.quote(
                        f"Hi {member_name},\n\n"
                        f"This is a friendly reminder about the book you loaned from Liana's Library.\n\n"
                        f"Book Title: '{book_title}'\n"
                        f"Loan Date: {borrow_date_str}\n"
                        f"Loan ID: {loan_id}\n\n"
                        f"Please ensure you return the book on time. If you have any questions, please contact us.\n\n"
                        f"Thank you,\nLiana's Library Team"
                    )
                    mailto_link = f"mailto:{member_email}?subject={email_subject}&body={email_body}"

                    st.markdown(f"<a href='{mailto_link}' target='_blank'><button style='background-color:#007bff;color:white;padding:10px 20px;border-radius:8px;border:none;cursor:pointer;'>Send Email Reminder</button></a>", unsafe_allow_html=True)


    st.markdown("---")

    # Bulk Upload Loans
    st.subheader("Bulk Upload Loans (CSV)")
    uploaded_loans_file = st.file_uploader("Upload CSV file for Loans", type=["csv"], key="upload_loans_csv")
    if uploaded_loans_file:
        try:
            loans_df_upload = pd.read_csv(uploaded_loans_file)
            st.write("Preview of uploaded data:")
            st.dataframe(loans_df_upload.head())
            if st.button("Process Bulk Loan Upload", key="process_bulk_loans"):
                results = bulk_insert_loans_from_df(loans_df_upload)
                for res in results:
                    if "Error" in res:
                        st.error(res)
                    else:
                        st.success(res)
                st.success("Bulk loan upload process completed.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

st.markdown("---")
st.markdown("Use this page to add, update, or delete records in your library database.")
