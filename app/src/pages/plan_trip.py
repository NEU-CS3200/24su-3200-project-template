import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Time to plan your next trip!")
st.write('')
st.write('')

# should have a statement for adding a new trip

flight_budget_col = st.columns(1)
with flight_budget_col[0]:
    flight_budget = st.number_input('Maximum flight budget:')

logger.info(f'flight_budget = {flight_budget}')

if st.button('Find flights! ',
              type = 'primary',
              use_container_width = True):
    try:
        flights = requests.get(f'http://api:4000/f/price/{flight_budget}')
        st.dataframe(flights)
    except Exception as e:
        st.error(f"An error occurred: {e}")




with st.form("Create a trip"):
    city_name = st.text_input("Input the city you would like to travel to.")
    group_size = st.number_input("List group size.")
    start_date = st.date_input("Insert start date of your trip.")
    end_date = st.date_input("Insert end date of your trip.")
    name = st.text_input("Insert the name of your trip.")
    restaurant_budget = st.number_input("What is your budget for eating out at restaurants?")
    attraction_budget = st.number_input("What is your budget for attractions?")
    hotel_budget = st.number_input("What is your hotel budget?")
    num_of_nights = st.number_input("How many nights is your trip?")
    

    submitted = st.fomr_submit_button("Submit")

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
        data['num_of_nights'] = num_of_nights
        st.write(data)

        requests.post('http://api:4000/t/trip', json=data)