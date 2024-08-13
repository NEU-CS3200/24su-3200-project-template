import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# View all adoption data")
adoption_data = requests.get('http://api:4000/adp/adoptions').json()
df = pd.DataFrame(adoption_data)
df = df[['name', 'petID', 'firstName', 'lastName', 'adopterID', 'email', 'phone', 'adoption_date',\
        'adoptionID']]
df.rename(columns={'name': 'Pet Name'}, inplace=True)
st.write(df)
