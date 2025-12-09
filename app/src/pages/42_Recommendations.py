import streamlit as st
import requests
import time
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

# CSS Styling for logout button
st.markdown("""
<style>
/* Logout button styling */
section[data-testid="stSidebar"] > div:last-child .stButton > button,
div[data-testid="stSidebar"] > div:last-child .stButton > button {
    background-color: #328E6E !important;
    color: #E1EEBC !important;
    height: 3em !important;
    width: 100% !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: none !important;
    margin-top: 1rem !important;
}
section[data-testid="stSidebar"] > div:last-child .stButton > button:hover,
div[data-testid="stSidebar"] > div:last-child .stButton > button:hover {
    background-color: #2a7359 !important;
    border-color: #328E6E !important;
}
</style>
""", unsafe_allow_html=True)

API_BASE = "http://api:4000/t"

st.title('✨ Personalized Recommendations')
st.caption("Based on your order history - items in categories, sizes, and styles you've ordered before")

user_id = st.session_state.get('user_id', 8)

response = requests.get(f"{API_BASE}/recommendations/{user_id}")
if response.status_code == 200:
    try:
        recommendations = response.json()
    except:
        recommendations = []
else:
    recommendations = []

if recommendations:
    st.success(f"**🎉 Found {len(recommendations)} personalized recommendations for you!**")
    if len(recommendations) < 3:
        st.caption(f"_Showing {len(recommendations)} recommendations (up to 3)_")
    
    category_emojis = {
        'shoes': '👟', 't-shirt': '👕', 'jacket': '🧥', 'dress': '👗', 'jeans': '👖',
        'sweater': '🧶', 'coat': '🧥', 'skirt': '👗', 'hoodie': '🧥', 'shirt': '👔',
        'blouse': '👔', 'pants': '👖', 'shorts': '🩳', 'top': '👚', 'vest': '🎽',
        'blazer': '👔', 'tank top': '👕'
    }
    
    def get_category_emoji(category):
        if category:
            category_lower = str(category).lower()
            return category_emojis.get(category_lower, '👕')
        return '👕'
    
    with st.container(height=600, border=True):
        for item in recommendations:
            category = item.get('Category', '')
            emoji = get_category_emoji(category)
            reason = item.get('RecommendationReason', 'Recommended for you')
            
            with st.expander(f"{emoji} {item.get('Title', 'Item')}", expanded=False):
                st.info(f"💡 **Why:** {reason}")
                
                cols = st.columns([2, 1])
                
                with cols[0]:
                    st.write(f"**Category:** {item.get('Category', 'N/A')}")
                    st.write(f"**Description:** {item.get('Description', 'N/A')}")
                    st.write(f"**Size:** {item.get('Size', 'N/A')}")
                    st.write(f"**Condition:** {item.get('Condition', 'N/A')}")
                    st.write(f"**Owner:** {item.get('OwnerName', 'N/A')}")
                    if item.get('Tags'):
                        st.write(f"**Tags:** {item.get('Tags', 'N/A')}")
                    st.write(f"**Posted:** {item.get('ListedAt', 'N/A')}")
                
                with cols[1]:
                    item_id = item.get('ItemID')
                    
                    check_response = requests.get(f"{API_BASE}/check_request/{user_id}/{item_id}")
                    is_requested = check_response.json().get('requested', False)
                    
                    if is_requested:
                        st.info("✅ Already requested")
                    else:
                        if st.button("Request Item", key=f"rec_{item_id}", type="primary"):
                            response = requests.post(f"{API_BASE}/request_item", json={"item_id": item_id, "user_id": user_id})
                            if response.status_code == 201:
                                st.toast(f"Requested: {item['Title']}", icon="✅")
                                time.sleep(1.5)
                                st.rerun()
else:
    st.info("No personalized recommendations available. Start ordering items to get recommendations based on your preferences!")