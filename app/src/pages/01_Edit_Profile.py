import logging

logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks


@st.cache_data
def get_available_preferences():
    return requests.get("http://api:4000/preferences").json()


# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.title("Update Profile + Preferences")

USER_ID = 1

user_data = requests.get("http://api:4000/customers/" + str(USER_ID)).json()

pref_data = get_available_preferences()

prices = pref_data["prices"]
cuisines = pref_data["cuisines"]
diets = pref_data["diets"]
formalities = pref_data["formalities"]

with st.form("update_profile"):
    st.write("#### Basic Info")

    st.text_input("First Name:", value=user_data["firstName"])
    st.text_input("Middle Initial:", value=user_data["middleInitial"], max_chars=1)
    st.text_input("Last Name:", value=user_data["lastName"])
    st.text_input("Email:", value=user_data["email"])
    st.number_input(
        "Longitude:",
        min_value=-180.0,
        max_value=180.0,
        value=user_data["longitude"],
        step=1e-6,
        format="%.6f",
    )
    st.number_input(
        "Latitude:",
        min_value=-180.0,
        max_value=180.0,
        value=user_data["latitude"],
        step=1e-6,
        format="%.6f",
    )

    st.write("#### Preferences")

    def format_price(price_id):
        return f"${prices[price_id]['rating']}: {prices[price_id]['description']}"

    current_price_pref = [str(p) for p in user_data["prices"]]
    st.multiselect("Prices", prices.keys(), current_price_pref, format_func=format_price)

    def create_multiselect(label, prefs, default_data):
        def format_pref(pref_id):
            return f"{prefs[pref_id]['name']} - {prefs[pref_id]['description']}"

        formatted_default_data = [str(p) for p in default_data]
        st.multiselect(label, prefs.keys(), formatted_default_data, format_func=format_pref)

    create_multiselect("Cuisines", cuisines, user_data["cuisine"])
    create_multiselect("Diets", diets, user_data["diet"])
    create_multiselect("Formality", formalities, user_data["formality"])

    st.form_submit_button("Update")
