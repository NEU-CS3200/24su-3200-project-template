import logging
import streamlit as st
from modules.nav import SideBarLinks

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

# CSS Styling
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

/* Page title */
.title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

/* Section subtitle */
.section-subtitle {
    color: #328E6E;
    font-size: 22px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 10px;
}

/* Buttons*/
div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 4em;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
    border-color: #328E6E;
}

/* Center columns properly */
[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)

# Logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="title">Swap into style and swap roles</div>', unsafe_allow_html=True)


# Admin
if st.button("🧑🏻‍💼  Admin", key="Admin", use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'admin'
    st.session_state['first_name'] = 'Aisha'
    logger.info("Logging in as Admin Persona")
    st.switch_page('pages/00_AdminDash.py')

st.markdown("<br>", unsafe_allow_html=True)

# Data Analyst
if st.button("👩🏽‍💻  Data Analyst", key="Data Analyst", use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['first_name'] = 'Blair'
    logger.info("Logging in as Data Analyst Persona")
    st.switch_page('pages/00_DADash.py')

st.markdown("<br>", unsafe_allow_html=True)

# Swapper
if st.button("🙋🏼‍♂️  Swapper", key="Swapper", use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'swapper'
    st.session_state['first_name'] = 'Andrea'
    logger.info("Logging in as Swapper Persona")
    st.switch_page('pages/00_SwapperDash.py')

st.markdown("<br>", unsafe_allow_html=True)

# Taker
if st.button("🙋🏼‍♀️  Taker", key="Taker", use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'taker'
    st.session_state['first_name'] = 'Alice'
    st.session_state['user_id'] = 8
    logger.info("Logging in as Taker Persona")
    st.switch_page('pages/00_TakerDash.py')
