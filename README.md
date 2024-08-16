# Project Pal- Summer 2024 CS3200 Project

## Team Members
- Spring Yan - yan.sp@northeastern.edu
- Blythe Berlinger - berlinger.b@northeastern.edu
- Nathaniel Yee - yee.n@northeastern.edu
- Corey Wang - wang.cor@northeastern.edu
- David Ku - ku.d@northeastern.edu

## Project Links
- [GitHub Repository](https://github.com/NathanielYee/24su-3200-project-pal)
- INSERT DEMO VIDEO LINK HERE!!!!!!!!!

## About

Project Pal is a web-based application designed to aid in group formation and management for students, professors and TAs in various class sizes. It connects students with like-minded peers based on their schedules, skills and past experiences, ensuring they are matched with and ideal team for class projects. Professors can monitor groups, submissions and update groups as needed. TA's are assigned to student groups based on their specialities and availability and monitor them so the projects run smoothly. 

This project was constructed using Streamlit for the frontend, Flask for the REST API backend, and MySQL for the database. The project implements a Role-Based Access Control (RBAC) system, allowing different features to be shown depending on the user's role (Student, TA, or Professor)

## Elevator Pitch

In large lecture-based classes, finding the right group mates for a project can be a daunting task. Introducing Project Pal—your solution to this challenge. Project Pal connects students with like-minded peers based on their schedules, interests, and past experiences, ensuring they find the ideal team. Our app will recommend matches for students with profiles, and then pair them accordingly. Then, our app will alert the professor and recommend TAs to be assigned to groups based on their office hours and expertise. The professor will also be able to monitor groups’ progress and capacity as well as be able to assign TAs to groups or go directly to students to resolve any conflicts. Teaching assistants are equipped with features to manage multiple groups and provide immediate support to students. With skill matching, professors can assign TAs to groups that would benefit the most from their expertise, ensuring each team has the guidance it needs to succeed. 

## Getting Started
Before running this project, ensure you have the following installed
1. Docker
2. Docker Compose

## Setting Up The Project
1. Log in to GitHub or Create an Account if you do not have yet. 
2. Clone the Repository:
    - git clone https://github.com/NathanielYee/24su-3200-project-pal.git
    - cd 24su-3200-project-pal
3. Set up the Environment:
    - Navigate to the api directory: cd api
    - Create a .env file based on the .env.template file provided in the 'api' folder. The .env should contain your database connection details and password that you set. 
    - The fields shoudl appear like this:
        SECRET_KEY=someCrazyS3cR3T!Key.!
        DB_USER=rost
        DB_HOST=db
        DB_PORT=3306
        DB_NAME=Project_pal
        MYSQL_ROOT_PASSWORD=YourPasswordHere  # Replace with your own password

4. Build and Start Docker Containers
    - Return to root directory of project and run in the console:docker-compose up -d --build
    - This will start the MySQL database, Flask API, and Streamlit frontend in detached mode. The MySQL schema and sample data will be automatically populated using the SQL files in teh 'database-files' directory. 

5. Accessing the Application
    - Once all containers are running in Docker (green), you c an access the Streamlit app by searching 'http://localhost:8501' in your web browser.
 

## Role-Based Access Control (RBAC) System
Our application served three primary personas:
    1. Student (Sam)
    2. Teaching Assistant (Timmy)
    3. Professor (Mark)

### How It Works
When a user logs in, they are presented with a choice of roles to assume. Depending on the role selected, the application will display customized sidebar links and pages to match the functionality required for that specific role. 



### Getting Started with the RBAC 
1. We need to turn off the standard panel of links on the left side of the Streamlit app. This is done through the `app/src/.streamlit/config.toml` file.  So check that out. We are turning it off so we can control directly what links are shown. 
1. Then I created a new python module in `app/src/modules/nav.py`.  When you look at the file, you will se that there are functions for basically each page of the application. The `st.sidebar.page_link(...)` adds a single link to the sidebar. We have a separate function for each page so that we can organize the links/pages by role. 
1. Next, check out the `app/src/Home.py` file. Notice that there are 3 buttons added to the page and when one is clicked, it redirects via `st.switch_page(...)` to that Roles Home page in `app/src/pages`.  But before the redirect, I set a few different variables in the Streamlit `session_state` object to track role, first name of the user, and that the user is now authenticated.  
1. Notice near the top of `app/src/Home.py` and all other pages, there is a call to `SideBarLinks(...)` from the `app/src/nav.py` module.  This is the function that will use the role set in `session_state` to determine what links to show the user in the sidebar. 
1. The pages are organized by Role.  Pages that start with a `0` are related to the *Political Strategist* role.  Pages that start with a `1` are related to the *USAID worker* role.  And, pages that start with a `2` are related to The *System Administrator* role. 


## Deploying An ML Model (Totally Optional for CS3200 Project)

*Note*: This project only contains the infrastructure for a hypothetical ML model. 

1. Build, train, and test your ML model in a Jupyter Notebook. 
1. Once you're happy with the model's performance, convert your Jupyter Notebook code for the ML model to a pure python script.  You can include the `training` and `testing` functionality as well as the `prediction` functionality.  You may or may not need to include data cleaning, though. 
1. Check out the  `api/backend/ml_models` module.  In this folder, I've put a sample (read *fake*) ML model in `model01.py`.  The `predict` function will be called by the Flask REST API to perform '*real-time*' prediction based on model parameter values that are stored in the database.  **Important**: you would never want to hard code the model parameter weights directly in the prediction function.  tl;dr - take some time to look over the code in `model01.py`.  
1. The prediction route for the REST API is in `api/backend/customers/customer_routes.py`. Basically, it accepts two URL parameters and passes them to the `prediction` function in the `ml_models` module. The `prediction` route/function packages up the value(s) it receives from the model's `predict` function and send its back to Streamlit as JSON. 
1. Back in streamlit, check out `app/src/pages/11_Prediction.py`.  Here, I create two numeric input fields.  When the button is pressed, it makes a request to the REST API URL `/c/prediction/.../...` function and passes the values from the two inputs as URL parameters.  It gets back the results from the route and displays them. Nothing fancy here. 

 