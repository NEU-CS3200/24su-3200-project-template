import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Student Analytics Dashboard")
st.markdown("---")


API_BASE_URL = "http://web-api:4000"
WAGE_DATA_ENDPOINT = f"{API_BASE_URL}/workedatpos/wagedata"

def fetch_wage_data():
    """Fetch wage data from the REST API"""
    try:
        response = requests.get(WAGE_DATA_ENDPOINT, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

wage_data = fetch_wage_data()

if wage_data:
    df = pd.DataFrame(wage_data)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Positions", len(df))
    
    with col2:
        avg_pay = df['avgPay'].mean() if 'avgPay' in df.columns else 0
        st.metric("Average Pay", f"${avg_pay:.2f}/hr")
    
    with col3:
        max_pay = df['maxSalary'].max() if 'maxSalary' in df.columns else 0
        st.metric("Highest Pay", f"${max_pay:.2f}/hr")
    
    with col4:
        total_coops = df['numPreviousCoops'].sum() if 'numPreviousCoops' in df.columns else 0
        st.metric("Total Previous Co-ops", total_coops)
    
    st.markdown("---")
    
    # Display the wage data table
    st.subheader("Co-op Position Wage Data")
    st.markdown("Data from past co-op positions showing company names, position titles, and salary ranges.")
    
    # Format the data for better display
    if not df.empty:
        # Rename columns for better display
        display_df = df.copy()
        if 'companyName' in display_df.columns:
            display_df = display_df.rename(columns={'companyName': 'Company Name'})
        if 'positionTitle' in display_df.columns:
            display_df = display_df.rename(columns={'positionTitle': 'Position Title'})
        if 'minSalary' in display_df.columns:
            display_df = display_df.rename(columns={'minSalary': 'Min Salary ($/hr)'})
        if 'maxSalary' in display_df.columns:
            display_df = display_df.rename(columns={'maxSalary': 'Max Salary ($/hr)'})
        if 'avgPay' in display_df.columns:
            display_df = display_df.rename(columns={'avgPay': 'Average Pay ($/hr)'})
        if 'numPreviousCoops' in display_df.columns:
            display_df = display_df.rename(columns={'numPreviousCoops': 'Previous Co-ops'})
        
        # Format salary columns to 2 decimal places
        salary_columns = ['Min Salary ($/hr)', 'Max Salary ($/hr)', 'Average Pay ($/hr)']
        for col in salary_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].round(2)
        
        # Display the table
        st.dataframe(display_df, use_container_width=True)
        
        # Add some visualizations
        st.markdown("---")
        st.subheader("Pay Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Average Pay ($/hr)' in display_df.columns:
                st.bar_chart(display_df.set_index('Position Title')['Average Pay ($/hr)'].head(10))
                st.caption("Top 10 Positions by Average Pay")
        
        with col2:
            if 'Company Name' in display_df.columns and 'Average Pay ($/hr)' in display_df.columns:
                company_avg = display_df.groupby('Company Name')['Average Pay ($/hr)'].mean().sort_values(ascending=False).head(10)
                st.bar_chart(company_avg)
                st.caption("Top 10 Companies by Average Pay")
    
else:
    st.warning("No wage data available. Please check if the API is running and accessible.")
    st.info("Make sure the backend API is running on port 4000.")


