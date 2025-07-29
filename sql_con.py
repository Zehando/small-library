# sql_con.py

from sqlalchemy import create_engine
import os # Import the os module to access environment variables

# It's crucial to use environment variables for sensitive data like database URLs.
# Streamlit Cloud (and other deployment platforms) allow you to set these securely.
#
# Replace the placeholder URL with your actual Neon.tech connection string.
# The `os.environ.get()` function attempts to retrieve the DATABASE_URL
# environment variable. If it's not found (e.g., when running locally without
# setting the env var), it falls back to the provided default string.
#
# IMPORTANT: When deploying to Streamlit Cloud, you MUST set DATABASE_URL
# as a secret in their deployment settings. DO NOT hardcode your actual
# Neon.tech password here if you intend to push this to a public GitHub repo.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_UZhzq9vjWm6b@ep-super-wave-a9g9p785-pooler.gwc.azure.neon.tech/neondb?sslmode=require"
)

# Create the SQLAlchemy engine using the PostgreSQL connection string
# The `pool_pre_ping=True` argument helps maintain connections in cloud environments
# by checking if the connection is still alive before using it.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Note: You no longer need to create tables here as they are already
# created in your Neon.tech database.
# The create_tables() function (if it existed) should be removed or commented out.
