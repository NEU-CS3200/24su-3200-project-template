import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Add a New Pet to the Database")

# Create a form to add a pet for adoption
with st.form("Input New Pet Information"):
    pet_id = st.number_input("Input New Pet's ID:", step=1)
    pet_name = st.text_input("Input New Pet's Name:")
    pet_status = st.checkbox("Is the pet available for adoption?")
    pet_species = st.text_input("Input New Pet's Species:")
    pet_breed = st.text_input("Input New Pet's Breed:")
    pet_birthday = st.date_input("Input New Pet's Birthday:")
    pet_age = st.number_input("Input New Pet's Age:", step=1)
    pet_alive = st.checkbox("Is the pet alive?")

    submitted = st.form_submit_button("Submit")

    if submitted:
      data = {}
      data['petID'] = pet_id
      data['name'] = pet_name
      data['adoption_status'] = pet_status
      data['species'] = pet_species
      data['breed'] = pet_breed
      data['birthday'] = pet_birthday.isoformat()
      data['age'] = pet_age
      data['is_alive'] = pet_alive
      st.write(data)

      requests.post('http://localhost:4000/p/pets', json=data) 

