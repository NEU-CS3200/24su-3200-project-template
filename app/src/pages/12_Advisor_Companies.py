import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

# API endpoint configuration
API_BASE_URL = "http://web-api:4000"
RATING_ENDPOINT = f"{API_BASE_URL}/workedatpos/company-ratings"
ALL_COMPANIES_ENDPOINT = f"{API_BASE_URL}/companyProfiles"

st.title('Company Partnerships')

st.markdown("""
This page displays company partnerships sorted by their average student ratings.
Companies with higher ratings appear first, showing detailed statistics including min/max ratings and total ratings.
""")

def fetch_company_ratings():
    """Fetch company profiles sorted by rating from the API"""
    try:
        response = requests.get(RATING_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Failed to fetch rating data: {response.status_code}")
            st.error(f"Response: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []

def fetch_all_companies():
    """Fetch all company profiles from the API"""
    try:
        response = requests.get(ALL_COMPANIES_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Failed to fetch company data: {response.status_code}")
            st.error(f"Response: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []

def display_company_ratings():
    """Display company ratings in a table format"""
    # Fetch data from API
    with st.spinner("Fetching company data..."):
        rated_companies = fetch_company_ratings()
        all_companies = fetch_all_companies()
    
    # Display summary statistics
    if rated_companies:
        total_rated = len(rated_companies)
        
        # Ensure ratings are converted to float and handle any None values
        ratings = []
        for comp in rated_companies:
            rating = comp.get('avgRating')
            if rating is not None:
                try:
                    ratings.append(float(rating))
                except (ValueError, TypeError):
                    continue
        
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            top_company = max(rated_companies, key=lambda x: float(x.get('avgRating', 0)) if x.get('avgRating') is not None else 0)
        else:
            avg_rating = 0
            top_company = rated_companies[0] if rated_companies else None
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Companies with Ratings", total_rated)
        with col2:
            st.metric("Overall Average Rating", f"{avg_rating:.1f}/5.0")
        with col3:
            company_name = top_company.get('companyName', 'N/A') if top_company else 'N/A'
            st.metric("Top Rated Company", company_name)
        
        st.divider()
    
    # Add filtering options
    if rated_companies:
        # Since workedatpos endpoint doesn't have industry, we'll skip industry filtering
        filtered_companies = rated_companies
    else:
        filtered_companies = []
    
    # Display companies with ratings
    if filtered_companies:
        st.subheader("🏆 Highest Performing Companies")
        st.markdown("*Sorted by average rating by past coops (highest to lowest)*")
        
        # Create a DataFrame-like display using Streamlit
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1, 1, 1, 1])
        
        with col1:
            st.write("**Company ID**")
        with col2:
            st.write("**Company Name**")
        with col3:
            st.write("**Industry**")
        with col4:
            st.write("**Avg Rating**")
        with col5:
            st.write("**# of Ratings**")
        with col6:
            st.write("**Min**")
        with col7:
            st.write("**Max**")
        
        st.divider()
        
        for company in filtered_companies:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1, 1, 1, 1])
            
            with col1:
                st.write(company.get('companyProfileId', 'N/A'))
            with col2:
                st.write(f"**{company.get('companyName', 'N/A')}**")
            with col3:
                st.write(company.get('companyIndustry', 'N/A'))
            with col4:
                avg_rating = company.get('avgRating', 0)
                if avg_rating is not None:
                    try:
                        avg_rating = float(avg_rating)
                        # Display rating with color coding
                        if avg_rating >= 4.0:
                            st.success(f"{avg_rating:.1f}/5.0 ⭐")
                        elif avg_rating >= 3.0:
                            st.info(f"{avg_rating:.1f}/5.0")
                        else:
                            st.warning(f"{avg_rating:.1f}/5.0")
                    except (ValueError, TypeError):
                        st.write("Invalid rating")
                else:
                    st.write("No ratings")
            with col5:
                total_ratings = company.get('totalRatings', 0)
                st.write(f"{total_ratings}")
            with col6:
                min_rating = company.get('minRating', 'N/A')
                if min_rating is not None:
                    st.write(f"{min_rating:.1f}")
                else:
                    st.write("N/A")
            with col7:
                max_rating = company.get('maxRating', 'N/A')
                if max_rating is not None:
                    st.write(f"{max_rating:.1f}")
                else:
                    st.write("N/A")
            
            st.divider()
            
# Main content
try:
    display_company_ratings()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logger.error(f"Error in display_company_ratings: {str(e)}")


