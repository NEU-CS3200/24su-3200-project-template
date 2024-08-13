########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

trip = Blueprint('trip', __name__)

# Getting trips
@trip.route('/trip', methods =['GET'])
def get_trip():
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    cursor.execute('Select start_date, end_date, name, restaurant_budget, attraction_budget, num_of_nights, city_id FROM trip') #CHANGE FROM CITY_ID TO CITY_NAME
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

