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
        - SECRET_KEY=someCrazyS3cR3T!Key.!
        - DB_USER=rost
        - DB_HOST=db
        - DB_PORT=3306
        - DB_NAME=Project_pal
        - MYSQL_ROOT_PASSWORD=YourPasswordHere  # Replace with your own password

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

1. Custom Sidebar Links
    - A custom module, nav.py, located in the app/src/modules/ directory, defines the sidebar links for each role. Functions within this module, such as SideBarLinks(), are responsible for dynamically generating the appropriate navigation options when a user logs in.
2. Role Selection and Session Management
    - The application's home page, app/src/Home.py, presents users with buttons to log in as Sam (Student), Timmy (TA), or Mark (Professor). Upon selection, the system sets various session state variables like role, first_name, and authenticated to track the user's session.
3. Role Specific Pages
    - The pages within the application are organized by role:
        - Student (Sam): Pages are found in app/src/pages/00_student_Home.py and other associated files, providing features like finding groupmates, updating majors, and managing tasks.
        - Teaching Assistant (Timmy): Pages are under app/src/pages/10_Ta_Home.py and other associated files, offering tools to find students by availability, specialty, and updating availability.
        - Professor (Mark): Pages are within app/src/pages/20_Professor_Home.py and related files, enabling functionalities such as updating student groups, monitoring sections, and viewing student submissions.
4. RBAC in Action
    - Each page is tailored to display the correct options and functionalities based on the role of the logged-in user. For instance:
        - Students can find peers based on specific criteria and update their profiles.
        - TAs can find students that match their availability or specialty and update their availability.
        - Professors can manage student groups, view students in their sections, and check submissions.
    - The RBAC implementation ensures that users only see and interact with the pages and functionalities relevant to their roles, promoting a secure and streamlined user experience.



