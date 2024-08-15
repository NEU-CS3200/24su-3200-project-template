import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Streamlit app title
st.title("Hotel Email Finder")

# Input field to enter the hotel name
name_col = st.columns(1)
with name_col[0]:
    name = st.text_input("Enter the hotel name:")

# Button to find the email
if st.button("Get Hotel Email"):
    if not name:
        st.error("Please enter the hotel name.")
    else:
        # Make a request to the API (assuming it requires destination and hotel name, but we will only use hotel name here)
        response = requests.get(f'http://api:4000/h/get_email/{name}').json()
        logger.info(f"response = {response}")
        st.dataframe(response)

# Creates a form to create a marketing campaign based off of the most clicked on
st.title("Create a Hotel Marketing Campaign")
st.write('')
st.write('')


with st.form("Create Marketing Campaign"):
    name = st.text_input("Input the name of the Marketing Campaign you would like to create.")
    employee_id = st.number_input("Insert your employee id. ")
    description = st.text_input("Ad description")
    budget = st.number_input("What is the budget for this Ad?", min_value=0.0, format="%.2f")
    code = st.number_input("Insert promotion code")
    discount_amount = st.number_input("What is the discount amount?", min_value=0.0, format="%.2f")
    
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        data['name'] = name
        data['employee_id'] = employee_id
        data['description'] = description
        data['budget'] = budget
        data['code'] = code
        data['discount_amount'] = discount_amount

        st.write(data)

        try:
            response = requests.post(f'http://api:4000/mc/add_marketing_campaign/{st.session_state["id"]}', json = data)
            st.success("Marketing Campaign details submitted successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

