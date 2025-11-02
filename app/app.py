import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path
from yaml.loader import SafeLoader
from screen_feedback import render_feedback_ui
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Page Config (MUST be the first st command) ---
# Moved from inside the 'if' block to the top of the script.
# st.set_page_config(page_title="My App", layout="wide")

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Exam Feedback AI",
    page_icon="📝",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Exam Feedback AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Get instant feedback on student answers</h4>", unsafe_allow_html=True)
st.write("---")

# --- Load Configuration ---
# The config.yaml file MUST be in the same directory as this script
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

# --- Initialize Authenticator (v0.4.2 syntax) ---
# This is the specific syntax for streamlit-authenticator v0.4.2
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


if st.session_state.get('authentication_status'):

    authenticator.logout(location='sidebar')
    render_feedback_ui()
    # st.write(f'Welcome *{st.session_state.get("name")}*')
    
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')




