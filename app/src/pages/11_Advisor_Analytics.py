import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Advisor Analytics page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Get the user_id from session state
advisor_user_id = st.session_state.get("user_id", None)

if advisor_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# Function to fetch advisor data from API
def fetch_advisor_data(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        logger.info(f"Fetching advisor data from API: status_code={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Received advisor data: {data}")
            return data[0] if data and len(data) > 0 else None
        else:
            logger.warning(f"API returned status {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching advisor data: {e}")
        # Fallback data if API is not available
        return {
            'userId': 31,
            'firstName': 'Sarah',
            'lastName': 'Martinez',
            'email': 's.martinez@neu.edu'
        }

# Function to fetch placement analytics data
def fetch_placement_analytics(advisor_id):
    # Define fallback sample data for demonstration
    fallback_data = [
        {
            'firstName': 'Charlie', 'lastName': 'Stout', 'gradYear': '2026', 'major': 'Computer Science',
            'college': 'Khoury College of Computer Sciences', 'gpa': 3.8, 'status': 'Accepted',
            'positionTitle': 'Software Engineer Intern', 'salary': 75000, 'companyName': 'TechCorp',
            'industry': 'Technology'
        },
        {
            'firstName': 'Isabella', 'lastName': 'Anderson', 'gradYear': '2025', 'major': 'Business Administration',
            'college': "D'Amore-McKim School of Business", 'gpa': 3.6, 'status': 'Rejected',
            'positionTitle': 'Marketing Analyst', 'salary': 65000, 'companyName': 'MarketPro',
            'industry': 'Marketing'
        },
        {
            'firstName': 'Liam', 'lastName': 'Williams', 'gradYear': '2025', 'major': 'Mechanical Engineering',
            'college': 'College of Engineering', 'gpa': 3.9, 'status': 'Accepted',
            'positionTitle': 'Engineering Intern', 'salary': 70000, 'companyName': 'EngineerCorp',
            'industry': 'Manufacturing'
        },
        {
            'firstName': 'Sophia', 'lastName': 'Brown', 'gradYear': '2027', 'major': 'Data Science',
            'college': 'Khoury College of Computer Sciences', 'gpa': 3.7, 'status': 'Accepted',
            'positionTitle': 'Data Analyst', 'salary': 68000, 'companyName': 'DataFlow Analytics',
            'industry': 'Technology'
        },
        {
            'firstName': 'Emma', 'lastName': 'Davis', 'gradYear': '2026', 'major': 'Finance',
            'college': "D'Amore-McKim School of Business", 'gpa': 3.5, 'status': 'Rejected',
            'positionTitle': 'Financial Analyst', 'salary': 72000, 'companyName': 'FinanceFirst',
            'industry': 'Finance'
        },
        {
            'firstName': 'Noah', 'lastName': 'Miller', 'gradYear': '2025', 'major': 'Computer Science',
            'college': 'Khoury College of Computer Sciences', 'gpa': 3.4, 'status': 'Accepted',
            'positionTitle': 'Full Stack Developer', 'salary': 80000, 'companyName': 'WebSolutions',
            'industry': 'Technology'
        }
    ]

    try:
        response = requests.get(f"{API_BASE_URL}/advisors/{advisor_id}/analytics/placement-data")
        logger.info(f"Fetching placement analytics from API: status_code={response.status_code}")
        if response.status_code == 200:
            api_data = response.json()
            logger.info(f"Received placement data: {len(api_data) if api_data else 0} records")
            if api_data:  # If API returns data, use it
                logger.info(f"Successfully fetched {len(api_data)} placement records from API")
                return api_data
            else:  # If API returns empty array, use fallback data
                logger.info("API returned empty data, using fallback sample data")
                return fallback_data
        else:
            # API returned error status, use fallback data
            logger.warning(f"API returned status {response.status_code}, using fallback sample data")
            return fallback_data
    except Exception as e:
        logger.error(f"Error fetching placement analytics: {e}")
        logger.info("Using fallback sample data due to API error")
        return fallback_data

# Fetch data
advisor_data = fetch_advisor_data(advisor_user_id)
placement_data = fetch_placement_analytics(advisor_user_id)



if advisor_data:
    # Header
    st.title("📊 Student Analytics Dashboard")
    st.subheader(f"Welcome back, {advisor_data['firstName']}!")

    if placement_data:
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(placement_data)

        # Create two-column layout: sidebar (25%) and main content (75%)
        sidebar_col, main_col = st.columns([1, 3])

        with sidebar_col:
            st.markdown("### 🔍 Filter Controls")

            # Extract unique values for filters
            unique_grad_years = sorted(df['gradYear'].unique().tolist())
            unique_colleges = sorted(df['college'].unique().tolist())
            unique_majors = sorted(df['major'].unique().tolist())
            unique_industries = sorted(df['industry'].unique().tolist())

            # Filter controls with "All" option
            grad_year_options = ["All"] + unique_grad_years
            selected_grad_years = st.multiselect(
                "Graduation Year",
                options=grad_year_options,
                default=["All"],
                help="Select graduation years to include in analysis",
                key="grad_years_filter"
            )

            college_options = ["All"] + unique_colleges
            selected_colleges = st.multiselect(
                "Department/College",
                options=college_options,
                default=["All"],
                help="Select colleges/departments to include",
                key="colleges_filter"
            )

            major_options = ["All"] + unique_majors
            selected_majors = st.multiselect(
                "Major",
                options=major_options,
                default=["All"],
                help="Select student majors to include",
                key="majors_filter"
            )

            industry_options = ["All"] + unique_industries
            selected_industries = st.multiselect(
                "Industry",
                options=industry_options,
                default=["All"],
                help="Select job industries to include",
                key="industries_filter"
            )

            gpa_range = st.slider(
                "GPA Range",
                min_value=0.0,
                max_value=4.0,
                value=(0.0, 4.0),
                step=0.1,
                help="Select GPA range for filtering students",
                key="gpa_range_filter"
            )

        with main_col:
            # Apply filters to data with real-time updates
            # Handle "All" option for each filter
            if "All" in selected_grad_years:
                grad_year_filter = unique_grad_years
            else:
                grad_year_filter = selected_grad_years

            if "All" in selected_colleges:
                college_filter = unique_colleges
            else:
                college_filter = selected_colleges

            if "All" in selected_majors:
                major_filter = unique_majors
            else:
                major_filter = selected_majors

            if "All" in selected_industries:
                industry_filter = unique_industries
            else:
                industry_filter = selected_industries

            # Apply filters to DataFrame
            filtered_df = df[
                (df['gradYear'].isin(grad_year_filter)) &
                (df['college'].isin(college_filter)) &
                (df['major'].isin(major_filter)) &
                (df['industry'].isin(industry_filter)) &
                (df['gpa'] >= gpa_range[0]) &
                (df['gpa'] <= gpa_range[1])
            ]

            if not filtered_df.empty:
                    # Summary statistics
                    total_records = len(filtered_df)
                    accepted_applications = len(filtered_df[filtered_df['status'] == 'Accepted'])
                    completed_coops = len(filtered_df[filtered_df['status'] == 'Completed'])
                    success_rate = ((accepted_applications + completed_coops) / total_records) * 100 if total_records > 0 else 0
                    avg_hourly_successful = filtered_df[filtered_df['status'].isin(['Accepted', 'Completed'])]['salary'].mean()

                    # Display summary statistics
                    stat_col1, stat_col2, stat_col3 = st.columns(3)
                    with stat_col1:
                        st.metric("Total Records", total_records)
                    with stat_col2:
                        st.metric("Success Rate", f"{success_rate:.1f}%")
                    with stat_col3:
                        if not pd.isna(avg_hourly_successful):
                            st.metric("Avg Hourly Pay (Successful)", f"${avg_hourly_successful:.2f}")
                        else:
                            st.metric("Avg Hourly Pay (Successful)", "N/A")

                    st.markdown("---")

                    # Create interactive scatterplot
                    fig = go.Figure()

                    # Add successful experiences (green dots) - both Accepted applications and Completed co-ops
                    successful_data = filtered_df[filtered_df['status'].isin(['Accepted', 'Completed'])]
                    if not successful_data.empty:
                        fig.add_trace(go.Scatter(
                            x=successful_data['gpa'],
                            y=successful_data['salary'],
                            mode='markers',
                            marker=dict(color='green', size=10, opacity=0.7),
                            name='Accepted Apps & Completed Co-ops',
                            hovertemplate='<b>%{customdata[0]} %{customdata[1]}</b><br>' +
                                        'GPA: %{x:.2f}<br>' +
                                        'Position: %{customdata[2]}<br>' +
                                        'Company: %{customdata[3]}<br>' +
                                        'Hourly Pay: $%{y:.2f}<br>' +
                                        'Status: %{customdata[4]}<extra></extra>',
                            customdata=successful_data[['firstName', 'lastName', 'positionTitle', 'companyName', 'status']].values
                        ))

                    # Add rejected applications (red dots)
                    rejected_data = filtered_df[filtered_df['status'] == 'Rejected']
                    if not rejected_data.empty:
                        fig.add_trace(go.Scatter(
                            x=rejected_data['gpa'],
                            y=rejected_data['salary'],
                            mode='markers',
                            marker=dict(color='red', size=10, opacity=0.7),
                            name='Rejected Applications',
                            hovertemplate='<b>%{customdata[0]} %{customdata[1]}</b><br>' +
                                        'GPA: %{x:.2f}<br>' +
                                        'Position: %{customdata[2]}<br>' +
                                        'Company: %{customdata[3]}<br>' +
                                        'Hourly Pay: $%{y:.2f}<br>' +
                                        'Status: %{customdata[4]}<extra></extra>',
                            customdata=rejected_data[['firstName', 'lastName', 'positionTitle', 'companyName', 'status']].values
                        ))

                    # Update layout
                    fig.update_layout(
                        title="Student Placement Analytics: GPA vs Hourly Pay",
                        xaxis_title="Student GPA",
                        yaxis_title="Hourly Pay (USD)",
                        yaxis=dict(tickformat='$,.2f'),
                        xaxis=dict(range=[0, 4.0]),
                        height=600,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )

                    # Display the plot
                    st.plotly_chart(fig, use_container_width=True)

                    # Legend explanation
                    st.markdown("""
                    **Legend:** 🟢 Green = Accepted Applications & Completed Co-ops | 🔴 Red = Rejected Applications

                    **How to use:** Hover over data points to see detailed information about each application or completed co-op.
                    Use the filter controls on the left to focus on specific student groups or criteria.
                    """)

            else:
                st.warning("No data matches the selected filters. Please adjust your filter criteria.")
    else:
        st.info("No placement data available for analysis.")

else:
    st.error("Unable to load advisor data. Please try again later.")
    st.info("If this problem persists, please contact the system administrator.")