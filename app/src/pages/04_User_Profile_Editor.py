import logging

logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks
from datetime import date, datetime

st.set_page_config(layout="wide")

SideBarLinks()

try:
    response = requests.get(f"http://api:4000/users/{st.session_state['profile_id']}")
    if response.status_code == 200:
        data = response.json()[0]
        st.title(f"{data['name']}'s Profile")
        st.image(data["profilePic"], width=150)
        with st.form("edit_profile"):
            fname = st.text_input("First Name:", value=str(data["firstName"]))
            mname = st.text_input("Middle Name:", value=str(data["middleName"]))
            lname = st.text_input("Last Name:", value=str(data["lastName"]))
            pname = st.text_input("Preferred Name:", value=str(data["preferredName"]))
            pnouns = st.text_input("Pronouns:", value=str(data["pronouns"]))
            bday = st.date_input(
                "Birthday:",
                value=datetime.strptime(
                    data["birthday"], "%a, %d %b %Y %H:%M:%S %Z"
                ).date(),
            )
            email = st.text_input("Email:", value=str(data["email"]))
            phone = st.text_input("Phone Number:", value=str(data["mobile"]))
            bio = st.text_area("Bio:", value=data["profile"])

            submit_button = st.form_submit_button("Save changes")

            if submit_button:
                bday = bday.strftime("%Y-%m-%d")
                req_data = {
                    "firstName": fname,
                    "middleName": mname,
                    "lastName": lname,
                    "preferredName": pname,
                    "pronouns": pnouns,
                    "birthday": bday,
                    "email": email,
                    "mobile": phone,
                    "profile": bio,
                }
                with requests.Session() as session:
                    try:
                        session.headers.update({"Content-Type": "application/json"})
                        response = session.put(
                            f"http://api:4000/users/{st.session_state['profile_id']}",
                            json=req_data,
                        )
                        logger.info(response.json())
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to server: {str(e)}")
                    st.success("Profile updated successfully")

        if st.button("Go back", type="primary", use_container_width=True):
            st.switch_page("pages/03_User_Profile.py")


except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to server: {str(e)}")
