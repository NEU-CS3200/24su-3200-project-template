import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="Admin Analytics Dashboard")
SideBarLinks()

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-success {
        background-color: #28a745;
    }
    
    .status-error {
        background-color: #dc3545;
    }
    
    .api-status {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 2rem;
    }
    
    .section-header {
        color: #495057;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Admin Analytics Dashboard</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Comprehensive overview of system metrics and user analytics</p>
</div>
""", unsafe_allow_html=True)

# Test the API endpoints
test_url = "http://web-api:4000"

# User Metrics Section
st.markdown('<h2 class="section-header">👥 User Analytics</h2>', unsafe_allow_html=True)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

with col1:
    # Fetch student count first
    try:
        response = requests.get(f"{test_url}/users/count/students", timeout=5)
        if response.status_code == 200:
            data = response.json()
            student_count = data.get('student_count', 0)
        else:
            student_count = 0
    except Exception as e:
        student_count = 0
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👨‍🎓 Students</div>
        <div class="metric-value">{student_count}</div>
        <div style="color: #28a745; font-size: 0.9rem;">Active in system</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Fetch advisor count first
    try:
        response = requests.get(f"{test_url}/users/count/advisors", timeout=5)
        if response.status_code == 200:
            data = response.json()
            advisor_count = data.get('advisor_count', 0)
        else:
            advisor_count = 0
    except Exception as e:
        advisor_count = 0
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👨‍🏫 Advisors</div>
        <div class="metric-value">{advisor_count}</div>
        <div style="color: #17a2b8; font-size: 0.9rem;">Academic support</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Fetch employer count first
    try:
        response = requests.get(f"{test_url}/users/count/employers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            employer_count = data.get('employer_count', 0)
        else:
            employer_count = 0
    except Exception as e:
        employer_count = 0
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏢 Employers</div>
        <div class="metric-value">{employer_count}</div>
        <div style="color: #ffc107; font-size: 0.9rem;">Industry partners</div>
    </div>
    """, unsafe_allow_html=True)

# Summary Section
st.markdown("---")
st.markdown('<h2 class="section-header">📈 System Summary</h2>', unsafe_allow_html=True)

# Calculate total users
try:
    student_response = requests.get(f"{test_url}/users/count/students", timeout=5)
    advisor_response = requests.get(f"{test_url}/users/count/advisors", timeout=5)
    employer_response = requests.get(f"{test_url}/users/count/employers", timeout=5)
    
    if all(r.status_code == 200 for r in [student_response, advisor_response, employer_response]):
        student_data = student_response.json()
        advisor_data = advisor_response.json()
        employer_data = employer_response.json()
        
        total_users = student_data.get('student_count', 0) + advisor_data.get('advisor_count', 0) + employer_data.get('employer_count', 0)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", total_users, delta=None)
        
        with col2:
            st.metric("System Status", "Online", delta="✓", delta_color="normal")
        
        with col3:
            st.metric("API Response", "Healthy", delta="< 5s", delta_color="normal")
        
        with col4:
            st.metric("Last Updated", datetime.now().strftime("%H:%M"), delta="Live", delta_color="normal")
            
    else:
        st.warning("⚠️ Some metrics are unavailable. Please check system connectivity.")
        
except Exception as e:
    st.error(f"❌ Unable to fetch system summary: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <small>Admin Analytics Dashboard • Real-time monitoring • Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</small>
</div>
""", unsafe_allow_html=True)


