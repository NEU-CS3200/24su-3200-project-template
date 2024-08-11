import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import os

SideBarLinks()

st.write("# Accessing a REST API from Within Streamlit")

"""
Simply retrieving data from a REST API running in a separate Docker Container.

If the container isn't running, this will be very unhappy. But the Streamlit app 
should not totally die.
"""

# Base URL for user data
base_url = 'http://localhost:4000/u/users'

# Display all users
database_name = os.getenv('DB_NAME')  
st.write(f"Database Name: {database_name}")
try:
    response = requests.get(base_url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Users:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))

# Ask the user to input a User ID
user_id = st.text_input("Enter User ID to fetch specific user details", "")

# Conditionally make API request based on user input for specific user details
if user_id:
    specific_url = f"{base_url}/{user_id}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data for user ID:")
            st.json(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for user ID {user_id}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch user ID {user_id}:")
        st.text(str(e))
else:
    st.write("Enter a user ID above to fetch specific user details.")


st.write(f"Database Name: {database_name}")
url = 'http://localhost:4000/l/listings'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Users:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


listing_id = st.text_input("Enter Listings ID to fetch specific listings details", "")

# Conditionally make API request based on user input for specific user details
if listing_id:
    specific_url = f"{url}/{listing_id}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing user ID:")
            st.json(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_id}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_id}:")
        st.text(str(e))
else:
    st.write("Enter a listing ID above to fetch specific user details.")


url = 'http://localhost:4000/l/tenLeastExpensive'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Users:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


url = 'http://localhost:4000/l/tenMostExpensive'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Users:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


url = 'http://localhost:4000/l/tenLeastExpensive'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Users:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))




listing_state = st.text_input("Enter Listings state to fetch specific listings details", "")

# Conditionally make API request based on user input for specific user details
if listing_state:
    specific_url = f"{url}/{listing_state}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing state:")
            st.json(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_state}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_state}:")
        st.text(str(e))
else:
    st.write("Enter a listing ID above to fetch specific user details.")