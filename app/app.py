import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path
from yaml.loader import SafeLoader
from screen_feedback import render_feedback_ui
from screen_chat import render_chat_ui
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Anatomy AI Assistant",
    page_icon="assets/icon2.jpg",
    layout="wide"
)

# --- Load Configuration ---
config_path = Path(__file__).parent / "config.yaml"

try:
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("config.yaml not found. Please run create_config.py first.")
    st.stop()
except Exception as e:
    st.error(f"Error loading config.yaml: {e}")
    st.stop()

# --- Initialize Authenticator ---
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
except KeyError as e:
    st.error(f"Config file is missing a required key: {e}. Please check your config.yaml.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")
    st.stop()

try:
    authenticator.login(location='main')
    logger.info(st.session_state.get('authentication_status'))
except Exception as e:
    st.error(e)

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Feedback"

if st.session_state.get('authentication_status'):
    
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        authenticator.logout(location='sidebar')
        st.write("---")
        page = st.radio(
            "Go to",
            ["📝 Feedback", "💬 Chat"],
            index=0 if st.session_state.page == "Feedback" else 1
        )
        # Extract page name without emoji
        st.session_state.page = page.split(" ", 1)[1]
    
    # Render selected page
    if st.session_state.page == "Feedback":
        render_feedback_ui()
    elif st.session_state.page == "Chat":
        render_chat_ui()
    
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')