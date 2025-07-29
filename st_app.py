import streamlit as st
from sql_auth_functions import verify_password # Import the verification function
import random # For generating star positions

st.set_page_config(page_title="Lianas Library", page_icon="📚")

#Function to generate multiple box-shadows for stars
def generate_star_shadows(n, max_x=2000, max_y=2000):
    """Generates a string of multiple box-shadows for stars."""
    shadows = []
    for _ in range(n):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        shadows.append(f"{x}px {y}px #FFF")
    return ", ".join(shadows)

# Generate star shadows with different densities and sizes
shadows_small = generate_star_shadows(700) # 700 small stars
shadows_medium = generate_star_shadows(200) # 200 medium stars
shadows_big = generate_star_shadows(100) # 100 big stars

# Inject custom CSS for the starfield background
st.markdown(
    f"""
    <style>
    /* Global box-sizing */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box !important;
    }}

    /* Ensure HTML and Body take full height and are transparent for Streamlit's rendering */
    html, body {{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden; /* Hide main scrollbars */
        background-color: transparent !important; /* Ensure body itself is transparent */
    }}

    /* Target the main Streamlit app container for the base background */
    .stApp {{
        min-height: 100vh; /* Ensure it takes full viewport height */
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); /* Dark space gradient */
        color: #f2f2f2;  /* Text color */
        line-height: 1.6;
        font-family: 'lato', sans-serif; /* Using lato as per original Sass, ensure font is available or fallback */
        overflow: hidden; /* Keep app content within bounds, stars handle own overflow */
        position: relative; /* Needed for z-index and positioning internal elements */
    }}

    /* Starfield styles */
    #stars {{
        width: 1px;
        height: 1px;
        background: transparent;
        box-shadow: {shadows_small};
        animation: animStar 50s linear infinite;
    }}

    #stars:after {{
        content: " ";
        position: absolute;
        top: 2000px; /* Reset position for continuous animation */
        width: 1px;
        height: 1px;
        background: transparent;
        box-shadow: {shadows_small};
    }}

    #stars2 {{
        width: 2px;
        height: 2px;
        background: transparent;
        box-shadow: {shadows_medium};
        animation: animStar 100s linear infinite;
    }}

    #stars2:after {{
        content: " ";
        position: absolute;
        top: 2000px;
        width: 2px;
        height: 2px;
        background: transparent;
        box-shadow: {shadows_medium};
    }}

    #stars3 {{
        width: 3px;
        height: 3px;
        background: transparent;
        box-shadow: {shadows_big};
        animation: animStar 150s linear infinite;
    }}

    #stars3:after {{
        content: " ";
        position: absolute;
        top: 2000px;
        width: 3px;
        height: 3px;
        background: transparent;
        box-shadow: {shadows_big};
    }}

    /* Keyframe animation for stars moving downwards */
    @keyframes animStar {{
        from {{ transform: translateY(0px); }}
        to {{ transform: translateY(-2000px); }} /* Moves upwards to simulate background scrolling */
    }}

    /* CRUCIAL: Make Streamlit's internal containers transparent */
    [data-testid="stAppViewContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    .main,
    .block-container,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    /* Common Streamlit internal wrappers that might have backgrounds */
    div.st-emotion-cache-z5fcl4,
    div.st-emotion-cache-1c7y2kl,
    div.st-emotion-cache-1dp5vir,
    div.st-emotion-cache-1jmvea6,
    div.st-emotion-cache-1r6dm1s,
    div.st-emotion-cache-j7qwjs
    {{
        background-color: transparent !important;
    }}


    /* Sidebar styling */
    .stSidebar {{
        background-color: rgba(0, 0, 0, 0.3); /* Darker, semi-transparent sidebar */
        color: #f2f2f2;
        padding-top: 20px;
        z-index: 2; /* Ensure sidebar is above main content if needed */
    }}

    /* Adjust Streamlit component styling for readability on dark background */
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stLabel, .stSelectbox, .stTextInput, .stNumberInput, .stDateInput, .stTextArea {{
        color: #f2f2f2 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7); /* Stronger shadow for contrast */
    }}

    /* Adjust button styling for better visibility */
    .stButton>button {{
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
    }}

    .stButton>button:hover {{
        background-color: #45a049;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }}

    /* Adjust form styling */
    .stForm {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }}

    /* Streamlit tabs styling */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        font-size: 1.2rem;
        color: #f2f2f2;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab-list"] button {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }}
    .stTabs [data-baseweb="tab-list"] button:hover {{
        background-color: rgba(255, 255, 255, 0.2);
    }}
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background-color: rgba(255, 255, 255, 0.3);
        border-bottom: 3px solid #FFF; /* White highlight for tabs */
    }}

    /* Sidebar specific button styling */
    .stSidebar .stButton>button {{
        background-color: #007bff;
    }}
    .stSidebar .stButton>button:hover {{
        background-color: #0056b3;
    }}
    .stSidebar .stSlider .st-bd {{ /* Slider track */
        background-color: rgba(255, 255, 255, 0.3);
    }}
    .stSidebar .stSlider .st-be {{ /* Slider fill */
        background-color: #FFF; /* White fill for slider */
    }}
    .stSidebar .stSelectbox .st-bd {{ /* Selectbox background */
        background-color: rgba(255, 255, 255, 0.1);
    }}
    .stSidebar .stSelectbox .st-at {{ /* Selectbox text color */
        color: #f2f2f2;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Inject the HTML structure for the stars
st.markdown(
    """
    <div id='stars'></div>
    <div id='stars2'></div>
    <div id='stars3'></div>
    """,
    unsafe_allow_html=True
)


# Session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def login_page():
    st.title("🔐 Liana's Library Login")
    st.markdown("Please enter your credentials to access the library management system.")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username and password:
                is_valid, role = verify_password(username, password)
                if is_valid:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = role
                    st.success(f"Welcome, {username}! You are logged in as {role}.")
                    st.rerun() # Rerun to switch to the main app
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter both username and password.")

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()

# Main application logic
if not st.session_state.logged_in:
    login_page()
else:
    # Display logout button in sidebar once logged in
    st.sidebar.write(f"Logged in as: **{st.session_state.username}** ({st.session_state.user_role})")
    logout_button()

    # Define your navigation pages (only visible after login)
    overview_page1 = st.Page("p1_overview.py", title="Library Overview", icon=":material/dashboard:")
    datainput_page2 = st.Page("p2_datainput.py", title="Library Management", icon=":material/add_circle:")

    pg = st.navigation([overview_page1, datainput_page2])
    pg.run() # pg.run() is called here after login
