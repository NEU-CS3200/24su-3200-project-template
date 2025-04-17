import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(page_title="College Bookmark Insights", layout="wide")
SideBarLinks(show_home=True)

st.title("🎓 College Bookmark Insights")
st.write("See which schools are most interested in your discounts.")

# Simulated data of bookmarks
data = [
    {"College": "Northeastern University", "Discount Code": "COFFEE20", "Bookmarked Count": 42},
    {"College": "Boston University", "Discount Code": "PASTRY10", "Bookmarked Count": 27},
    {"College": "Harvard", "Discount Code": "ESPRESSO25", "Bookmarked Count": 13},
]

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("These insights help you know where to focus your marketing.")