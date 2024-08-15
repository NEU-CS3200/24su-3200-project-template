import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Time to plan your next trip!")
st.write('')
st.write('')

# should have a statement for adding a new trip

with st.form("Create a trip"):
    city_name = st.text_input("Input the city you would like to travel to.")
    group_size = st.number_input("List group size.", min_value=1, step=1, format="%d")
    start_date = st.date_input("Insert start date of your trip.")
    end_date = st.date_input("Insert end date of your trip.")
    name = st.text_input("Insert the name of your trip.")
    restaurant_budget = st.number_input("What is your budget for eating out at restaurants?", min_value=0.0, format="%.2f")
    attraction_budget = st.number_input("What is your budget for attractions?", min_value=0.0, format="%.2f")
    hotel_budget = st.number_input("What is your hotel budget?", min_value=0.0, format="%.2f")
    flight_budget = st.number_input("What is your flight budget?", min_value=0.0, format="%.2f")
    num_of_nights = st.number_input("How many nights is your trip?", min_value=1, step=1, format="%d")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        data['city_name'] = city_name
        data['group_size'] = group_size
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['name'] = name
        data['restaurant_budget'] = restaurant_budget
        data['attraction_budget'] = attraction_budget
        data['hotel_budget'] = hotel_budget
        data['flight_budget'] = flight_budget
        data['num_of_nights'] = num_of_nights
        st.write(data)

        try:
            response = requests.post('http://api:4000/t/trip', json = data)
            st.success("Trip details submitted successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

st.write('Based on your preferences, here are our recommendations!')
if st.button('Find your flight!',
              type = 'primary',
              use_container_width = True):
    result = requests.get('http://api:4000/f/get_flight').json()
    st.dataframe(results)

if st.button('Find your hotel!',
              type = 'primary',
              use_container_width = True):
    result = requests.get(f'http://api:4000/h/hotel/{city_name}').json()
    st.dataframe(results)

if st.button('Find your attraction!',
              type = 'primary',
              use_container_width = True):
    result = requests.get(f'http://api:4000/h/hotel/{city_name}').json()
    st.dataframe(results)