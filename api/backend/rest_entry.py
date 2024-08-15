import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask

from backend.db_connection import db
from backend.flights.flight_routes import flights
from backend.hotels.hotel_routes import hotel
from backend.attractions.attraction_routes import attractions
from backend.hotel_clicks.hotel_clicks_routes import hotel_clicks
from backend.trip.trip_routes import trip
from api.backend.attraction_clicks.attraction_clicks_routes import attraction_clicks
from backend.restaurant_clicks.restaurant_clicks_routes import restaurant_clicks
from backend.users.user_routes import users
from backend.ads.ads_routes import ads
from backend.promotions.promotions_route import promotions
from backend.employee.employee_routes import employees
from backend.marketing_campaign.marketing_campaign_routes import marketing_campaign
from backend.city_clicks.city_clicks_routes import city_clicks
from backend.city.city_routes import city
from backend.restaurant.restaurant_routes import restaurant

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')  # Change this to your DB name

    # Initialize the database object with the settings above. 
    db.init_app(app)

    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the Summer 2024 CS 3200 Project Template Repo</h1>"
    
    # Example route for testing streamlit
    @app.route("/data")
    def getData():
        data = {
            "staff": [
                {
                    "Name": "Mark Fontenot",
                    "role": "Instructor"
                },
                {
                    "Name": "Ashley Davis",
                    "role": "TA"
                },
                {
                    "Name": "Dylan Toplas",
                    "role": "TA"
                },
                {
                    "Name": "Hazelyn Aroian",
                    "role": "TA"
                },
                {
                    "Name": "Jared Lyon",
                    "role": "TA"
                },
                {
                    "Name": "Khanh Nguyen",
                    "role": "TA"
                },
                {
                    "Name": "Nathan Cheung",
                    "role": "TA"
                },
                {
                    "Name": "Nicole Contreras",
                    "role": "TA"
                },
                {
                    "Name": "Reid Chandler",
                    "role": "TA"
                },
                {
                    "Name": "Sai Kumar Reddy",
                    "role": "TA"
                }
            ]
        }
        return data
    
    app.logger.info('current_app(): registering blueprints with Flask app object.')

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(flights,     url_prefix='/f')
    app.register_blueprint(hotel,      url_prefix='/h')
    app.register_blueprint(attraction_clicks,    url_prefix='/ac')
    app.register_blueprint(attractions,    url_prefix='/a')
    app.register_blueprint(hotel_clicks,    url_prefix='/hc')
    app.register_blueprint(restaurant_clicks,    url_prefix='/rc')
    app.register_blueprint(trip,    url_prefix='/t')
    app.register_blueprint(users,    url_prefix='/u')
    app.register_blueprint(ads,    url_prefix='/ad')
    app.register_blueprint(promotions,    url_prefix='/p')
    app.register_blueprint(employees,    url_prefix='/e')
    app.register_blueprint(marketing_campaign,    url_prefix='/mc')
    app.register_blueprint(city_clicks, url_prefix='/cc')
    app.register_blueprint(city, url_prefix='/c')
    app.register_blueprint(restaurant, url_prefix='/r')


    # Don't forget to return the app object
    return app

