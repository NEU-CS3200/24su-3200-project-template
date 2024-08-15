import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

hotel_clicks = requests.get('http://api:4000/hc/hotel_clicks').json()

try:
  st.dataframe(hotel_clicks)
except:
  st.write("Could not connect to database to get hotel clicks.")

# st.write("# Accessing a REST API from Within Streamlit")
# products = requests.get('http:appi:4000/p/products').json()

# try: 
#   st.dataframe(products)
# except: 
#   st.write("Could not connect to database to retrieve products.")

try:
  hey = requests.get('http://api:4000/c/users').json()
  st.dataframe(hey)
except:
  st.write("Error!")

try:
  hey = requests.get('http://api:4000/h/hotel').json()
  st.dataframe(hey)
except:
  st.write("Error!")

"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""
#data = {} 
#try:
 # data = requests.get('http://api:4000/data').json()
#except:
# st.write("**Important**: Could not connect to sample api, so using dummy data.")
#  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

#st.dataframe(data)

