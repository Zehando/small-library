# 📚 Liana's Library Management System

A **Streamlit web application** for managing a small library's operations including members, books, and loans. Provides a user-friendly interface for CRUD operations, searching, and bulk data management.

---

## ✨ Features

- **User Authentication**
  - Secure login system for administrators and users.
- **Member Management**
  - Add, update, delete, and retrieve members.
  - Bulk upload via CSV.
  - Delete prevention if active loans exist.
- **Book Management**
  - Manage books with ISBN, title, author, etc.
  - Bulk upload and search by title/author.
  - Delete prevention if book is loaned out.
- **Loan Management**
  - Record, update, and delete loans.
  - Send email reminders for overdue loans.
  - Bulk upload via CSV.
- **Data Persistence**
  - PostgreSQL backend hosted on [Neon.tech](https://neon.tech).
- **Security**
  - Passwords hashed with `bcrypt`.

---

## 🔒 Password Hashing with Bcrypt

Passwords are hashed using `bcrypt` before storage.

- Each password is salted uniquely.
- Prevents rainbow table and brute-force attacks.
- Hashing logic in `sql_auth_functions.py`.

---

## 🚀 Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | Streamlit  |
| Backend   | Python     |
| Database  | PostgreSQL (Neon.tech) |
| ORM       | SQLAlchemy |
| Adapter   | `psycopg2-binary` |
| Security  | `bcrypt`   |
| Data      | Pandas     |
| Deploy    | Streamlit Cloud |

---

## 🛠️ Local Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Minimal `requirements.txt` should include:

```
streamlit
pandas
sqlalchemy
bcrypt
psycopg2-binary
```

### 4. Database Setup (PostgreSQL on Neon.tech)

#### a. Create a Neon Project & Database
- Sign in to [Neon.tech](https://neon.tech)
- Create a new project and database
- Copy the `postgresql://...` connection string

#### b. Import Initial SQL Dump
- Use [DBeaver](https://dbeaver.io/) or similar tool
- Connect with your Neon connection string
- Run the SQL dump and data in the SQL scripts folder to populate database and tables

#### c. Update Sequences
Run the following SQL commands to avoid ID conflicts:

```sql
SELECT setval('members_memberid_seq', (SELECT MAX(memberid) FROM members) + 1, false);
SELECT setval('loans_loanid_seq', (SELECT MAX(loanid) FROM loans) + 1, false);
SELECT setval('users_userid_seq', (SELECT MAX(userid) FROM users) + 1, false);
```

#### d. Create `.streamlit/secrets.toml`

```toml
# .streamlit/secrets.toml
DATABASE_URL = "postgresql://user:password@host:port/dbname?project=yourproject"
```

> **Never commit secrets.toml to public repos.**

---

## 🔐 Creating Users with Hashed Passwords

You can hash passwords using this script:

```python
import bcrypt

password = "your_password".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

Then, insert via SQL:

```sql
INSERT INTO users (username, passwordhash, role)
VALUES ('new_user', '$2b$12$EXAMPLEHASHSTRING...', 'user');
```

---

## ▶️ Run the Application

```bash
streamlit run st_app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub (including `requirements.txt` and `.streamlit/secrets.toml`)
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Log in and create a new app
4. Select your repo and main file (`st_app.py`)
5. Click **Deploy**

---

## 📂 Project Structure

```
📁 your-repo-name/
├── st_app.py                # Main entry point
├── p1_overview.py           # Library overview UI
├── p2_datainput.py          # Forms and data input logic
├── sql_auth_functions.py    # User authentication functions
├── sql_con.py               # Database connection
├── sql_crud_functions.py    # Create, Update, Delete logic
├── sql_read_functions.py    # Read/query functions
├── requirements.txt         # Dependencies
└── SQL scripts/
    └── liana_library_data.sql         # Configured scripts for PostgreSQL (data)
    └── liana_library_dump.sql         # Configured scripts for PostgreSQL (schema)
└── .streamlit/
    └── secrets.toml         # Secrets (e.g., DATABASE_URL)
```

---

## 📝 Usage

1. **Login:** Use provided credentials (e.g., `admin/admin`, `liana/user`)
2. **Navigate Tabs:** Switch between Members, Books, and Loans
3. **Manage Data:** Add, update, delete records or bulk upload CSVs

---

## 📄 License

[MIT License](LICENSE) 

---

## 🌟 Acknowledgments

Thanks to [Neon.tech](https://neon.tech) for free PostgreSQL hosting and the Streamlit community for awesome tools!

---

## 🤝 Contact

For any questions or feedback, feel free to reach out:

* **GitHub:** [@zehando](https://github.com/zehando)
* **LinkedIn:** [Sahand Azizi](https://www.linkedin.com/in/sahandazizi/)
* **Email:** azizisahand@gmail.com
