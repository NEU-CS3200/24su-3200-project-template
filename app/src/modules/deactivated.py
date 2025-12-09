import streamlit as st
import requests
import logging

logger = logging.getLogger(__name__)


def check_if_active(user_id):
    """
    Check if a user's account is active
    """
    try:
        response = requests.get(f'http://api:4000/admin/users/{user_id}', timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            user_info = user_data.get('data', user_data)
            is_active = user_info.get('IsActive', 1) == 1
            return is_active, user_info

        return True, None

    except Exception as e:
        logger.error(f"Error checking user status: {e}")
        return True, None  # Default to active on error


def spam_message():
    """
    Display spam posting messages
    """
    st.markdown("""
    <style>
    .deactivated-box {
        background-color: #fee;
        border: 3px solid #c33;
        border-radius: 12px;
        padding: 40px;
        margin: 50px auto;
        max-width: 600px;
        text-align: center;
    }
    
    .deactivated-box h1 {
        color: #c33;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .deactivated-box p {
        color: #666;
        font-size: 18px;
    }
    </style>
    
    <div class="deactivated-box">
        <h1>🚫 Account Deactivated</h1>
        <p>Your account has been deactivated due to spam listings.</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


def require_active_account():
    """
    Check if user is active
    """
    user_id = st.session_state.get('user_id')

    if not user_id:
        st.error("User ID not found in session")
        st.stop()

    is_active, _ = check_if_active(user_id)
    if not is_active:
        spam_message()