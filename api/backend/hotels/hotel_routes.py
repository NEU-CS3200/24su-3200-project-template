########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

hotel = Blueprint('hotel', __name__)

# Getting hotels
@hotel.route('/hotel', methods =['GET'])
def get_hotel():
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    cursor.execute('Select id, room_type, amenities, price_per_night, rating, city_id FROM hotel')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

