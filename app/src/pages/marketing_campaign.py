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

# Input field to enter the hotel destination
destination = st.text_input("Enter the destination:")

# Input field to enter the hotel name
name = st.text_input("Enter the hotel name:")

# Button to find the email
if st.button("Get Hotel Email"):
    if destination:
        # Request hotels data from the Flask backend
        response = requests.get(f'http://api:4000/h/hotel/{destination}')
        
        if response.status_code == 200:
            hotels = response.json()
            
            # Search for the hotel by name
            hotel_email = next((hotel['email'] for hotel in hotels if hotel['name'].lower() == name.lower()), None)
            
            if hotel_email:
                st.success(f"The email for {name} is: {hotel_email}")
            else:
                st.error("Hotel not found! Please check the name and try again.")
        else:
            st.error("Failed to retrieve hotels. Please try again later.")
    else:
        st.error("Please enter a destination.")





st.title("Create a Hotel Marketing Campaign")
st.write('')
st.write('')


with st.form("Create Marketing Campaign"):
    name = st.text_input("Input the name of the Marketing Campaign you would like to create.")
    description = st.text_input("Ad description")
    budget = st.number_input("What is the budget for this Ad?", min_value=0.0, format="%.2f")
    code = st.number_input("Insert promotion code")
    name = st.text_input("Insert the name of the promotion")
    discount_amount = st.number_input("What is the discount amount?", min_value=0.0, format="%.2f")
    
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        data['name'] = name
        data['description'] = description
        data['budget'] = budget
        data['code'] = code
        data['name'] = name
        data['discount_amount'] = discount_amount

        st.write(data)

        try:
            response = requests.post('http://api:4000/mc/marketing_campaign', json = data)
            st.success("Marketing Campaign details submitted successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

