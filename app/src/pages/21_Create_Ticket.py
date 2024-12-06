import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Create Ticket")

with st.form("ticket_data"):
    summary_input = st.text_input(
        "Summary",
        placeholder="State the issue and it's details",)
    submit_button = st.form_submit_button("Submit Ticket")
    if submit_button:
        if not summary_input:
            st.error("please enter a summary")
        else:
            req_data = {
                "summary": summary_input,
                "userId": st.session_state['id'],
            }
            with requests.Session() as session:
                try:
                    session.headers.update({"Content-Type": "application/json"})
                    response = session.post(
                        f"http://api:4000/create_help_ticket",
                        json=req_data,
                    )
                    logger.info(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
                st.success("Ticket submitted successfully")
