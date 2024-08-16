# Getaway Guru Project Repository

## Team Members
Catherine McKinley, Lauren Cummings, Layza Rodrigues, Veronica Song, and Willbert Christianto

## About

Getaway Guru is a comprehensive travel planning platform designed to simplify the trip-planning process for individuals and businesses alike. Our application combines advanced data analytics with user-friendly features to empower users to effortlessly discover and book ideal getaways tailored to their specific needs and preferences. 

Whether you're a budget-conscious student, a seasoned marketing analyst, or a corporate travel planner, Getaway Guru offers personalized recommendations. Our platform provides up-to-date information on flights, accomodations attractions, and dining options, ensuring a seamless and enjoyable travel experience. 

Getaway Guru aims to revolutionize the way people plan and book their trips, saving time, money, and stress. 

## Preprequisites 
-Docker 
-Docker Compose
-Python

## Installation: 
1 - Clone the resposiory
git clone https://github.com/your-username/getaway-guru.git
cd getaway-guru

2 - Create .env file
Create .env file in the project root based on the .env.example file with the following variable. Copy the .env.example file as .env. 

SECRET_KEY=you_secret_key
DB_USER=your_database_user
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
DB_Password = your_database_password

## Running the application: 
1 - Build and run containers: 
docker-compose up -d

## Loading the dataaset: 
Run the SQL file named consolidated_datasets.sql in order to load all the data into the database. 

## Accessing the application: 
You can access the application by opening a web browser and navigating to http://localhost:8501/

## Video Link:
https://drive.google.com/file/d/1SGQMYC08nzvxWj_x8QXJqAHlX5ynMSV6/view?usp=drive_link
