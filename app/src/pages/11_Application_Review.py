import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout="wide")

SideBarLinks()

if st.session_state["role"] == "student":
    st.title("Your Applications")
else:
    st.title("Student Applications")

data = None

# ADVISOR DATA

if st.session_state["role"] == "coop_advisor":
    try:
        with requests.Session() as s:
            response = s.get(
                f"http://api:4000/adv/advisors/{st.session_state['id']}/students"
            )
            apps = []
            if response.status_code == 200:
                stu = response.json()
                for student in stu:
                    response = s.get(
                        f"http://api:4000/stu/students/{student['studentId']}/applications"
                    )
                    if response.status_code == 200:
                        apps.append(response.json()[0])
            data = apps
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to applications API: {str(e)}")

# EMPLOYER DATA

if st.session_state["role"] == "employer":
    try:
        with requests.Session() as s:
            response = s.get(
                f"http://api:4000/emp/{st.session_state['company_id']}/positions"
            )
            apps = {}
            if response.status_code == 200:
                positions = response.json()
                for position in positions:
                    response = s.get(
                        f"http://api:4000/pos/positions/{position['id']}/applications"
                    )
                    if response.status_code == 200:
                        apps[position["summary"]] = response.json()
            data = apps
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to applications API: {str(e)}")

# STUDENT DATA

if st.session_state["role"] == "student":
    try:
        with requests.Session() as s:
            response = s.get(f"http://api:4000/users/{st.session_state['id']}")
            stu_id = response.json()[0]["studentId"]
            response = s.get(f"http://api:4000/stu/students/{stu_id}/applications")
            data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to applications API: {str(e)}")


def display_app(app):
    st.write(f"#### Summary: {app['summary']}")
    st.write(f"##### Question Responses: {app['questionResponse']}")
    st.write(f"##### GPA: {app['GPA']}")
    with requests.Session() as s:
        res = s.get(f"http://api:4000/app/applications/{app['id']}/work_experience")
        work_exp = res.json()
        res = s.get(f"http://api:4000/app/applications/{app['id']}/related_coursework")
        related_courses = res.json()
        res = s.get(f"http://api:4000/app/applications/{app['id']}/notable_skills")
        notable_skills = res.json()
        res = s.get(f"http://api:4000/app/applications/{app['id']}/user_refs")
        user_refs = res.json()
    st.write("##### Work Experience")
    if len(work_exp) != 0:
        for exp in work_exp:
            st.write(f"###### Name: {exp['name']}")
            st.write(f"###### Summary: {exp['summary']}")
    else:
        st.write("No work experience provided.")

    st.write("##### Coursework")
    if len(related_courses) != 0:
        for course in related_courses:
            st.write(f"###### Name: {course['name']}")
            st.write(f"###### Summary: {course['summary']}")
    else:
        st.write("No related coursework provided.")

    st.write("##### Notable Skills")
    if len(notable_skills) != 0:
        for skill in notable_skills:
            st.write(f"###### Name: {skill['name']}")
            st.write(f"###### Summary: {skill['summary']}")
    else:
        st.write("No notable skills provided.")

    st.write("##### User References")
    if len(user_refs) != 0:
        for ref in user_refs:
            st.write(f"###### Name: {ref['name']}")
            st.write(f"###### Email: {ref['email']}")
            st.write(f"###### Referrence: {ref['referral']}")
    else:
        st.write("No user references provided.")


if data is not None:
    if st.session_state["role"] == "student":
        button = st.button("Create New Application")
        if button:
            st.switch_page("pages/33_Application_Creator.py")
        if "button_states" not in st.session_state:
            st.session_state.button_states = {}
        for app in data:
            display_app(app)
            button_key = f"button_{app['id']}"
            if button_key not in st.session_state.button_states:
                st.session_state.button_states[button_key] = False
            if st.button("Edit", key=button_key):
                st.session_state.button_states[
                    button_key
                ] = not st.session_state.button_states[button_key]
                st.session_state["app_id"] = app["id"]
                st.switch_page("pages/32_Application_Editor.py")

    elif st.session_state["role"] == "employer":
        for key in data:
            st.write(f"### Applications for {key}:")
            for app in data[key]:
                display_app(app)
    elif st.session_state["role"] == "coop_advisor":
        for app in data:
            display_app(app)
