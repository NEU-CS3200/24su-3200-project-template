import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import os

SideBarLinks()

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


base_url = 'http://localhost:4000/u/usersgenders'

try:
    response = requests.get(base_url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All Genders:")
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
        st.write("All listings:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all listings. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


url = 'http://localhost:4000/l/listingsBeingRented'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All listings:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all listings. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


url = 'http://localhost:4000/l/listingsViews'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("All listings Views:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all listings. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))

url = 'http://localhost:4000/l/listings'
listing_id = st.text_input("Enter Listings ID to fetch specific listings details", "")

# Conditionally make API request based on user input for specific user details
if listing_id:
    specific_url = f"{url}/{listing_id}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing ID:")
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
        st.write("ten least expensive listings:")
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
        st.write("ten most expensive listings:")
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

url = 'http://localhost:4000/l/listingStates'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("States:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))




st.subheader("Create New Listing")
# Form to input data for new listing
with st.form(key='create_form'):
    id = st.text_input("ID")
    City = st.text_input("City")
    ZipCode = st.text_input("ZipCode")
    Street = st.text_input("Street")
    HouseNum = st.text_input("House Number")
    State = st.text_input("State")
    CurrPriceData = st.text_input("Current Price")
    PrevPriceData = st.text_input("Previous Price")
    PredictedFuturePriceData = st.text_input("Predicted Future Price")
    AreaId = st.text_input("Area ID")
    RealtorId = st.text_input("Realtor ID")
    Views = st.text_input("Views")
    BeingRented = st.selectbox("Is Being Rented?", ["Yes", "No"])

    submit_button = st.form_submit_button("Create Listing")

    if submit_button:
        new_listing = {
            "id": int(id),
            "BeingRented": BeingRented == "Yes",
            "City": City,
            "ZipCode": int(ZipCode),
            "Street": Street,
            "HouseNum": int(HouseNum),
            "State": State,
            "CurrPriceData": int(CurrPriceData),
            "PrevPriceData": int(PrevPriceData),
            "PredictedFuturePriceData": int(PredictedFuturePriceData),
            "AreaId": int(AreaId),
            "RealtorId": int(RealtorId),
            "Views": int(Views)
        }
        response = requests.post('http://localhost:4000/l/listings', json=new_listing)
        if response.status_code == 200:
            st.success("Listing created successfully!")
        else:
            st.error(f"Failed to create listing. Status code: {response.status_code}")


st.subheader("Update Existing Listing")


# Form to input data for updating an existing listing
with st.form(key='update_form'):
    listing_id = st.text_input("Listing ID", key="update_listing_id")
    new_price = st.text_input("New Price", key="update_price")
    new_views = st.text_input("New Views", key="update_views")

    submit_button = st.form_submit_button("Update Listing")

    if submit_button and listing_id:
        # Construct the dictionary with only the fields that are provided
        updated_data = {}
    if new_price.isdigit() and new_views.isdigit():
        updated_data = {
            "price": int(new_price),
            "Views": int(new_views)
        }

        # Only make the API call if there is at least one field to update
        if updated_data:
            # Ensure the URL matches the correct endpoint for updating listings by ID
            response = requests.put(f"http://localhost:4000/l/listings/{listing_id}", json=updated_data)
            if response.status_code == 200:
                st.success("Listing updated successfully!")
            else:
                st.error(f"Failed to update listing. Status code: {response.status_code}, Message: {response.text}")
        else:
            st.warning("No data provided to update. Please enter new values.")


st.subheader("Delete a Listing")
listing_id = st.text_input("Enter the Listing ID to delete:", key="delete_id")

if st.button("Delete Listing"):
    if listing_id:
        try:
            listing_id = int(listing_id)  # Convert to int to avoid invalid IDs
            response = requests.delete(f"http://localhost:4000/l/listings//{listing_id}")
            
            if response.status_code == 200:
                st.success("Listing deleted successfully!")
            elif response.status_code == 404:
                st.error("Listing not found. Please check the ID and try again.")
            else:
                st.error("Failed to delete listing. Please try again.")
        except ValueError:
            st.error("Please enter a valid integer ID.")
    else:
        st.warning("Please enter a Listing ID to delete.")

