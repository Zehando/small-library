import bcrypt
from sqlalchemy import text
from sql_con import engine 
import pandas as pd # Used for get_user_by_username

def hash_password(password):
    """Hashes a password using bcrypt."""
    # bcrypt.gensalt() generates a new salt each time, and the hash includes the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8') # Decode to string for storage

def verify_password(username, password):
    """
    Verifies a user's password against the stored hash in the database.
    Returns True if credentials are valid, False otherwise.
    """
    try:
        with engine.connect() as connection:
            query = text("SELECT PasswordHash, Role FROM Users WHERE Username = :username;")
            result = connection.execute(query, {'username': username}).fetchone()

            if result:
                stored_hash = result[0].encode('utf-8')
                role = result[1]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    return True, role
        return False, None # User not found or password incorrect
    except Exception as e:
        print(f"ERROR: verify_password failed: {e}")
        return False, None

def add_user(username, password, role):
    """
    Adds a new user to the Users table with a hashed password.
    Returns True, message on success, False, error message on failure.
    """
    try:
        with engine.connect() as connection:
            # Check if username already exists
            check_query = text("SELECT COUNT(*) FROM Users WHERE Username = :username;")
            if connection.execute(check_query, {'username': username}).scalar() > 0:
                return False, "Error: Username already exists."

            hashed_password = hash_password(password)
            insert_query = text("""
                INSERT INTO Users (Username, PasswordHash, Role)
                VALUES (:username, :password_hash, :role);
            """)
            connection.execute(insert_query, {
                'username': username,
                'password_hash': hashed_password,
                'role': role
            })
            connection.commit()
        return True, f"User '{username}' added successfully with role '{role}'."
    except Exception as e:
        return False, f"Error adding user: {e}"

def get_user_by_username(username):
    """Retrieves a user's details by username."""
    try:
        with engine.connect() as connection:
            query = text("SELECT UserID, Username, Role FROM Users WHERE Username = :username;")
            result_proxy = connection.execute(query, {'username': username})
            column_names = result_proxy.keys()
            result = result_proxy.fetchone()
            if result:
                return pd.DataFrame([result], columns=column_names)
            return pd.DataFrame()
    except Exception as e:
        print(f"ERROR: get_user_by_username failed for username {username}: {e}")
        return pd.DataFrame()

def update_user_password(username, new_password):
    """Updates a user's password."""
    try:
        hashed_password = hash_password(new_password)
        with engine.connect() as connection:
            query = text("UPDATE Users SET PasswordHash = :password_hash WHERE Username = :username;")
            result = connection.execute(query, {'password_hash': hashed_password, 'username': username})
            connection.commit()
            if result.rowcount > 0:
                return True, f"Password for user '{username}' updated successfully."
            return False, f"User '{username}' not found."
    except Exception as e:
        return False, f"Error updating password for user '{username}': {e}"

def delete_user(username):
    """Deletes a user from the Users table."""
    try:
        with engine.connect() as connection:
            query = text("DELETE FROM Users WHERE Username = :username;")
            result = connection.execute(query, {'username': username})
            connection.commit()
            if result.rowcount > 0:
                return True, f"User '{username}' deleted successfully."
            return False, f"User '{username}' not found."
    except Exception as e:
        return False, f"Error deleting user '{username}': {e}"
