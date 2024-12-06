import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
# COSINT: Revolutionizing Co-op Connections For Everyone.

Are you struggling to navigate the world of co-op opportunities? Whether you're a **student**, a **recruiter**, or a **school administrator**,
COSINT is here to streamline your co-op experience! 🎉

## Purpose
COSINT bridges the gap between students and recruiters while offering schools an efficient solution to manage their co-op programs. 
Our goal is to simplify the process for all parties by leveraging advanced data-driven techniques and a user-friendly platform.

### For Students 🧑‍🎓  
- Discover personalized co-op opportunities tailored to your skills and interests.  
- Stay organized with tools to track applications and flag top companies.  
- Receive notifications about new opportunities or updates on your applications.

### For Recruiters 🤔  
- Quickly sort and filter candidates using metrics like GPA, skills, and experience.  
- Access concise profiles to make informed decisions without sifting through resumes.  
- Streamline the hiring process with easy-to-use tools for managing applications.

### For Schools 🏫  
- Provide a centralized platform for students and recruiters to connect.  
- Equip advisors with metrics and tools to guide students effectively.  
- Monitor program success with insightful analytics and dashboards.

## Implementation
COSINT is built on a robust database design that ensures scalability and security. It utilizes:
- **SQL-powered relational databases** to store and manage user data efficiently.  
- **Dockerized containers** for easy deployment and maintenance.  
- **Python-based APIs and Streamlit interfaces** to deliver an intuitive user experience.

We’re committed to improving COSINT continuously—your feedback drives us forward! 🚀

    """
        )
