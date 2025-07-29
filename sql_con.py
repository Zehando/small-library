        # sql_con.py

        from sqlalchemy import create_engine
        import streamlit as st
        from sqlalchemy.engine import Engine # Import Engine type for type hinting

        _engine = None # Private variable to hold the engine instance

        def get_engine() -> Engine:
            """
            Returns a singleton SQLAlchemy engine instance.
            Initializes the engine only once.
            """
            global _engine
            if _engine is None:
                try:
                    # Read the database URL from Streamlit secrets
                    db_url = st.secrets["DATABASE_URL"]
                    _engine = create_engine(db_url)
                    # You can add a print statement here for debugging if needed
                    # print("DEBUG: Database engine initialized successfully.")
                except KeyError:
                    st.error("Database URL not found in Streamlit secrets. Please configure it.")
                    _engine = None # Ensure engine is None if secrets are missing
                except Exception as e:
                    st.error(f"Error initializing database engine: {e}")
                    _engine = None # Ensure engine is None on other errors
            return _engine

        # You no longer need a global 'engine' variable directly here.
        # Other modules will call get_engine() to obtain the engine.
