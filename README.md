# Liana's Library Management System

This is a Streamlit web application designed to manage a small library's operations, including members, books, and loans. It provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations, searching, and managing bulk data.

## ✨ Features

* **User Authentication:** Secure login system for administrators and users.
* **Member Management:**
    * Add new members with comprehensive details.
    * Retrieve and update existing member information.
    * Delete members (with a check for active loans).
    * Bulk upload members via CSV.
* **Book Management:**
    * Add new books with ISBN, title, author, publisher, year, and genre.
    * Retrieve and update existing book details.
    * Delete books (with a check for active loans).
    * Bulk upload books via CSV.
    * Search functionality for books by title or author.
* **Loan Management:**
    * Record new book loans, checking for book availability.
    * Update loan return dates.
    * Delete loan records.
    * Send email reminders for overdue loans.
    * Bulk upload loans via CSV.
* **Data Persistence:** Utilizes a PostgreSQL database (hosted on Neon.tech) for reliable data storage.

## 🔒 Security: Password Hashing

For enhanced security, user passwords are not stored directly in the database. Instead, they are hashed using the **bcrypt** algorithm.

* `bcrypt` is a strong, adaptive hashing function designed to be computationally intensive, making brute-force attacks difficult even with powerful hardware.
* Each password is hashed with a unique, randomly generated **salt**, which is stored along with the hash. This prevents "rainbow table" attacks and ensures that two users with the same password will have different hashes.
* The hashing logic is encapsulated in `sql_auth_functions.py`.

## 🚀 Technologies Used

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** PostgreSQL (Neon.tech)
* **Database ORM/Toolkit:** SQLAlchemy
* **PostgreSQL Adapter:** `psycopg2-binary`
* **Data Handling:** Pandas
* **Security:** `bcrypt` (for password hashing)
* **Deployment:** Streamlit Cloud

## 🛠️ Setup and Installation (Local Development)

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
(Replace your-username/your-repo-name with your actual GitHub repository path.)

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

Bash

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
Install the required Python packages:

Bash

pip install -r requirements.txt
Ensure your requirements.txt file contains the following minimal set of dependencies to avoid conflicts and large installations:

streamlit
pandas
sqlalchemy
bcrypt
psycopg2-binary
4. Database Setup (Neon.tech PostgreSQL)
This application uses a PostgreSQL database, ideally hosted on Neon.tech.

a. Create a Neon.tech Database
Go to Neon.tech and sign up or log in.

Create a new project and a new database (e.g., neondb).

Navigate to "Connection Details" and copy your "Connection String" (it will start with postgresql://).

b. Import Initial Data
Use a database client like DBeaver to connect to your Neon database using the copied connection string. Then, execute your initial SQL dump to populate the tables.

Important: Update Database Sequences
After importing your data, you must update the sequences for SERIAL primary keys to prevent "duplicate key" errors when adding new entries. Run the following SQL commands for each table with an auto-incrementing ID (members, loans, users):

SQL

SELECT setval('members_memberid_seq', (SELECT MAX(memberid) FROM members) + 1, false);
SELECT setval('loans_loanid_seq', (SELECT MAX(loanid) FROM loans) + 1, false);
SELECT setval('users_userid_seq', (SELECT MAX(userid) FROM users) + 1, false);
c. Configure Database Credentials
For local development, create a .streamlit folder in your project's root directory, and inside it, create a secrets.toml file.

Ini, TOML

# .streamlit/secrets.toml
DATABASE_URL = "postgresql://user:password@host:port/dbname?project=yourprojectname"
Replace the placeholder with your actual Neon.tech connection string.

5. Define Your Own Users (Optional)
The initial database dump provides admin and liana users. If you wish to define additional users directly in your database, you'll need to manually hash their passwords. You can use a Python script (like the setup_users.py provided earlier) or generate a hash and insert it via SQL.

Example of adding a user via SQL (requires a pre-hashed password):

First, you'd need to generate a bcrypt hash for your desired password. You can do this with a small Python script:

Python

import bcrypt
password = "my_new_secure_password".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode('utf-8'))
Copy the outputted hash (e.g., $2b$12$EXAMPLEHASHSTRING...).

Then, use this hash in an SQL INSERT statement in DBeaver:

SQL

INSERT INTO users (username, passwordhash, role)
VALUES ('new_user', '$2b$12$EXAMPLEHASHSTRING...', 'user');
Replace 'new_user' with the desired username, and the hash with the one you generated.

6. Run the Streamlit Application
Bash

streamlit run st_app.py
This will open the application in your web browser.

☁️ Deployment to Streamlit Cloud
To deploy your application to Streamlit Cloud for public access:

Ensure requirements.txt is clean: Verify it only contains the necessary packages as listed in step 3 above.

Secure your credentials: The DATABASE_URL in .streamlit/secrets.toml is automatically picked up and securely managed by Streamlit Cloud. Do NOT hardcode your database URL directly in your Python files if you're pushing to a public repository.

Push your code to GitHub: Ensure all your application files (including .streamlit/secrets.toml and requirements.txt) are committed and pushed to your GitHub repository.

Deploy on Streamlit Cloud:

Go to share.streamlit.io.

Log in with your GitHub account.

Click "New app" and select your repository, branch, and the main file (st_app.py).

Streamlit Cloud will automatically detect your secrets.toml and requirements.txt.

Click "Deploy!"

📂 Project Structure and File Breakdown
Here's an overview of what each file in your repository does:

st_app.py: This is the main Streamlit application entry point. It handles the initial setup (like set_page_config), the login/authentication logic, and then uses st.navigation to display the different pages of your application (p1_overview.py and p2_datainput.py) after a successful login. It also contains the custom CSS for the starfield background.

p1_overview.py: This file likely contains the Streamlit code for your "Library Overview" page, which would display summaries, statistics, or lists of members, books, and loans using the read functions.

p2_datainput.py: This file contains the Streamlit code for the "Data Input & Management" page. It includes all the forms and logic for adding, retrieving, updating, and deleting members, books, and loans, as well as the bulk upload functionalities.

requirements.txt: This file lists all the Python packages that your Streamlit application depends on. Streamlit Cloud (and pip) uses this file to install the necessary libraries for your app to run.

sql_auth_functions.py: This module handles all user authentication-related functions. It includes hash_password (using bcrypt), verify_password, and functions for adding, retrieving, updating, and deleting users from the users table.

sql_con.py: This file is responsible for establishing the connection to your PostgreSQL database using SQLAlchemy. It reads the database URL from Streamlit's secrets.

sql_crud_functions.py: This module contains the core database interaction logic for Create, Update, and Delete operations across your members, books, and loans tables. It also includes helper functions for checking record existence and bulk inserts.

sql_read_functions.py: This module contains functions specifically for Reading (retrieving) data from your members, books, and loans tables. It provides functions to get all records, active loans, and search books.

.streamlit/secrets.toml: This directory and file are used by Streamlit Cloud to securely store sensitive information, such as your database connection string, without exposing it directly in your public code.

📝 Usage
Login: Access the application and log in using your credentials (e.g., admin/admin or liana/user if you used the provided dump).

Navigate Tabs: Use the tabs (Members, Books, Loans) to switch between different management sections.

Perform Operations: Use the forms within each tab to add new records, retrieve data for updates, modify existing entries, or delete records.

Bulk Upload: Use the CSV upload functionality for large data imports.

🤝 Contributing
Feel free to fork this repository, open issues, or submit pull requests.
