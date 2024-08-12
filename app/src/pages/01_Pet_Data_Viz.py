import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Adoptable Pet Data')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# get the pets from the database
pets = requests.get('http://localhost:4000/p/pets').json()

try: 
    pets = [pet for pet in pets if pet['adoption_status'] == 0 and pet['is_alive'] == 1]
    st.dataframe(pets)
except: 
    st.write('Could not connect to database to retrieve pet data')    


# get the countries from the world bank data
# with st.echo(code_location='above'):
#    countries:pd.DataFrame = wb.get_countries()
   
#    st.dataframe(countries)

# the with statment shows the code for this block above it 
# with st.echo(code_location='above'):
#    arr = np.random.normal(1, 1, size=100)
#    test_plot, ax = plt.subplots()
#    ax.hist(arr, bins=20)

#    st.pyplot(test_plot)


#with st.echo(code_location='above'):
#    slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
#    data_crosstab = pd.crosstab(slim_countries['region'], 
#                                slim_countries['incomeLevel'],  
#                                margins = False) 
#    st.table(data_crosstab)

#if st.button('See aniamals',
#             type='primary',
#             use_container_width=True):
#  results = requests.get('http://api:4000/p/pets').json()
#  st.dataframe(results)
#if st.button('See agencies',
#             type='primary',
#             use_container_width=True):
#  results = requests.get('http://api:4000/a/agencies').json()
#  st.dataframe(results)
