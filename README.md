# FitHub: A Sustainable Clothing Trading Platform
# A CS 3200 Group Project Fall 2025 

Demo Video: [Demo Video!](https://www.youtube.com/watch?v=BqDdCF2K0Co)

Group Members:

Micah Cheng

William Cramer

London Jones 

Yurika Kan

Samuel Yao


FitHub is a digital clothing exchange platform designed to help people refresh their wardrobes sustainably. Instead of buying new clothes or engaging in bidding wars on platforms like Depop or Ebay, FitHub allows users to swap, take, or donate items based on personalized style and profiles. FitHub’s Flask REST API and Streamlit UI work together to support finding your dream wardrobe through analytical recommendations.

This program features:
   1. Smart Listings - Tagged items as "swap" or "take"
   2. Personalized Recommendations - User's style matching recommendations
   3. Order Tracking - Real-time package tracking
   4. Analytics Dashboard - For data-driven actions
   5. Admin Moderation - Content management and user tools

## User Roles

Fithub Supports four distinct user personas:

1. Admin (Aisha)
   Manages reported content and users
   Deactivates spam accounts
   Sends system accouncements
   Monitor platform health

2. Data Analyst (Blair)
   Can view listings and category stock
   Tracks late shipments
   Analyzes user demographics and engagement
   Generates platform metrics

3. Swapper (Kingsley)
   Posts clothing items for swap or take
   Browse and filters available items
   Requests swaps with other users
   Tracks incoming and outgoing packages
   Cancels pending swaps

4. Taker (Alexi)
   Browse free items ("takes")
   Filter by size, condition, or tags
   Get personalized recommendations
   Track incoming packages
   Cancel unfufilled requests

## Structure of the Repo

app/: 

Location of the Streamlit frontend.
Contains all user interface code, page layouts, and the main Home.py entry page inside app/src/

api/ :
The Flask REST API backend: 
Includes all server logic, business logic, and communication with the MySQL database.

database-files/ :

Contains SQL files that automatically initialize the MySQL database when the container is first created.

fithub.sql – Full schema and seed data for FitHub.

docker-compose.yml

Defines and runs all three containers: MySQL database, Flask backend API. Streamlit frontend

## Prerequisites

Before running the project:

A GitHub account

Git installed (CLI or GitHub Desktop)

Docker Desktop installed and running

A code editor 

Python 3.11 if you want to run the backend/frontend without Docker

##  Instructions 

How to Run the Project 

Follow these steps to run a fresh version of FitHub:

1. Pull the Latest Version of the Project

In a terminal:

git checkout main
git pull
Start All Containers:

Before running the project, create a valid .env file inside the api/ directory.

Create the file:

api/.env


Paste in these values:

SECRET_KEY=imsofitted
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=fithub

MYSQL_ROOT_PASSWORD=password


Once the .env file has been created, you may start the application using:

docker compose up -d --build

To verify that the system and test is working go to these links:

Frontend:

http://localhost:8501


Backend API:

http://localhost:4000


Test GET example:

http://localhost:4000/d/listings


To stop the services:

docker compose down
