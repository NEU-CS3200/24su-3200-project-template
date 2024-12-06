# Cosint: A Database Design Project

## Overview
Cosint is a data-driven platform designed to bridge the gap between students seeking cooperative education (co-op) opportunities and employers looking to hire talented interns. By leveraging advanced metrics and a centralized database, Cosint enhances connectivity and efficiency for students, employers, and advisors.

## Features
### For Students
- Personalized recruiter insights to help students prepare for interviews.
- Notification system for co-op opportunities and recruiter profile views.
- Tools to manage application statuses and flag top-choice companies.
- Profile updates for showcasing new skills and achievements.

### For Employers
- Quick filtering of applications based on GPA, skills, or experience.
- Easy access to student profiles for streamlined decision-making.
- Ability to maintain a record of accepted and rejected candidates.

### For Co-op Advisors
- Tools to track student applications and provide tailored advice.
- Metrics for analyzing past co-op performance to enhance future recommendations.

### For System Administrators
- Role-based access control for secure data handling.
- Ticketing system for issue resolution and platform monitoring.
- Notification alerts for suspicious activity and system outages.

## Personas
Cosint was designed with the following archetypes in mind:
- **Students**: Aspiring co-op candidates seeking tailored guidance and better application management.
- **Employers**: Companies aiming to identify and recruit top talent efficiently.
- **Co-op Advisors**: Educational professionals supporting students' co-op search journeys.
- **System Administrators**: Ensuring platform stability, security, and scalability.

## Database Design
- The global and localized ER diagrams define relationships between users, applications, companies, and positions.
- Relational database models include normalized tables for scalability and maintainability.
- The database supports CRUD operations, ensuring data integrity and relevance.

### SQL Highlights
- **Select Queries**: Retrieve user and position data.
- **Insert Queries**: Add new applications, bookmarks, and company profiles.
- **Update Queries**: Modify user profiles and position statuses.
- **Delete Queries**: Manage outdated or irrelevant data.

## Project Setup
### Prerequisites
- Docker installed and configured.
- Python development environment with Flask and Streamlit.
- Access to GitHub for version control.

### Instructions
1. **Clone the Repository**:
   ```bash  
   git clone <repository_url>
2. **Create a .env file in the api directory based on .env.template.**
3. **Start docker containers**:
   ```bash
   docker compose up -d
5. Access Application: Navigate to localhost:8501 for the Streamlit app. 
