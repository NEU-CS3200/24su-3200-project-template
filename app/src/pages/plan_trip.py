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