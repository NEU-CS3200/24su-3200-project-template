##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# Custom CSS for styling
st.markdown("""
<style>
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .user-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        transition: transform 0.2s ease-in-out;
    }
    
    .user-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.15);
    }
    
    .persona-title {
        color: #1e3a8a;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .persona-description {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    
    .welcome-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .feature-highlight {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header section
st.markdown('<h1 style="text-align: center; font-size: 5rem; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #ef4444 100%); '
'-webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold; margin-bottom: 1rem;">CoopAlytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Gateway to Co-op Data Analytics & Management</p>', unsafe_allow_html=True)

# Welcome section with feature highlights
st.markdown("""
<div class="welcome-section">
    <h3 style="color: #1e3a8a; margin-bottom: 1rem;">Welcome to CoopAlytics! 🎯</h3>
    <p style="color: #64748b; font-size: 1.1rem;">Select your role below to access personalized dashboards and insights</p>
</div>
""", unsafe_allow_html=True)

logger.info("Loading the Home page of the app")

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Choose Your User Role")
    
    # Student Persona
    st.markdown("""
    <div class="user-card">
        <div class="persona-title">🎓 Student Portal</div>
        <div class="persona-description">
            Access your application status, explore co-op opportunities, track your progress, 
            and get insights on industry trends and placement data.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Login as Student", 
                type='primary', 
                use_container_width=True,
                key="student_login"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'student'
        st.session_state['first_name'] = 'Charlie'
        st.session_state['user_id'] = 1
        logger.info("Logging in as Student Persona")
        st.switch_page('pages/00_Student_Home.py')

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Advisor Persona
    st.markdown("""
    <div class="user-card">
        <div class="persona-title">👨‍🏫 Academic Advisor Portal</div>
        <div class="persona-description">
            Monitor your advisees' application progress, analyze placement trends, 
            identify students needing support, and access comprehensive analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('Login as Academic Advisor', 
                type='primary', 
                use_container_width=True,
                key="advisor_login"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'advisor'
        st.session_state['first_name'] = 'Dr. Sarah'
        st.session_state['user_id'] = 31  # Sarah Martinez
        logger.info("Logging in as Academic Advisor Persona")
        st.switch_page('pages/10_Advisor_Home.py')

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Employer Persona
    st.markdown("""
    <div class="user-card">
        <div class="persona-title">🏢 Employer Portal</div>
        <div class="persona-description">
            Manage co-op positions, review applications, track hiring metrics, 
            and access candidate analytics to make informed hiring decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('Login as Employer', 
                type='primary', 
                use_container_width=True,
                key="employer_login"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'employer'
        st.session_state['first_name'] = 'Jennifer'
        logger.info("Logging in as Employer Persona")
        st.switch_page('pages/20_Employer_Home.py')

    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Administrator
    st.markdown("""
    <div class="user-card">
        <div class="persona-title">⚙️ System Administrator</div>
        <div class="persona-description">
            Access system-wide analytics, manage user accounts, monitor platform performance, 
            and maintain database integrity across all user roles.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('Login as System Administrator', 
                type='primary', 
                use_container_width=True,
                key="admin_login"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'administrator'
        st.session_state['first_name'] = 'SysAdmin'
        logger.info("Logging in as System Administrator Persona")
        st.switch_page('pages/30_Admin_Home.py')

# Footer section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="feature-highlight">
    <strong>🚀 Platform Features:</strong> Application Tracking • Placement Analytics • Company Ratings • 
    GPA vs Salary Insights • Industry Trends • Student Progress Monitoring
</div>
""", unsafe_allow_html=True)



