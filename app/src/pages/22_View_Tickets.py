import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()
st.title(f"Tickets")
with st.form("ticket_search"):
    ticket_value = student_input = st.text_input(
        "Search Tickets",
        placeholder="Enter Ticket Id#",
    )
    submit_button = st.form_submit_button("Search")
    df = None
    if submit_button:
        if not ticket_value:
            try:
                response1 = requests.get(f"http://api:4000/adm/tickets")
                if response1.status_code == 200:
                    if len(response1.json()) != 0:
                        df = pd.json_normalize(response1.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")
        else:
            logger.info(f"User form submitted with data: {ticket_value}")

            try:
                response = requests.get(f"http://api:4000/adm/tickets/{ticket_value}")
                if response.status_code == 200:
                    if len(response.json()) != 0:
                        df = pd.json_normalize(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

if df is not None:
    for index, row in df.iterrows():
        with st.expander(f"{row['helping']}: {row['summary']}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.write("##### Helping:")
            col1.write(f"{row['helping']}")
            col2.write("##### Admin Assigned:")
            col2.write(f"{row['assignedTo']}")
            col3.write("##### Issue Summary:")
            col3.write(f"{row['summary']}")
