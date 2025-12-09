import logging
logger = logging.getLogger(__name__)

import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

from modules.deactivated  import require_active_account
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = 8
require_active_account()

# Page config
st.set_page_config(layout="wide")

# Sidebar with logo
SideBarLinks()
add_logo("assets/FitHublogo.png")

# Log taker dashboard access
logger.info(f"Taker Dashboard loaded by {st.session_state.get('first_name', 'Unknown')}")

# CSS Styling
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

/* Page title */
.taker-title {
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


# Taker Dashboard UI
st.markdown(f'<div class="taker-title">👋 Welcome, Taker Alexi!</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">What would you like to do today?</div>', unsafe_allow_html=True)
st.write("")

# Main buttons - Browse and View Orders (half and half)
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("👕 Browse Feed", use_container_width=True, type="primary"):
        logger.info("Navigating to Browse Listings")
        require_active_account()
        st.switch_page('pages/40_Browse_Listings.py')

with col2:
    if st.button("📦 View My Orders", use_container_width=True, type="primary"):
        logger.info("Navigating to My Orders")
        require_active_account()
        st.switch_page('pages/41_My_Orders.py')

# Recommendations button
col1, col2 = st.columns([1, 1])

with col2:
    if st.button("✨ Recommendations", use_container_width=True, type="primary"):
        logger.info("Navigating to Recommendations")
        require_active_account()
        st.switch_page('pages/42_Recommendations.py')

