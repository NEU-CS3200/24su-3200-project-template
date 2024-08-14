from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

hotel = Blueprint('hotel', __name__)

# Getting hotels based on trip destination and total budget
@hotel.route('/hotel/<destination>', methods =['GET'])
def get_hotel(destination):
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    query = '''
        Select id, room_type, amenities, price_per_night, rating, city_id 
        FROM hotel JOIN trip ON hotel.city_id = trip.city_id
        WHERE city_id = ?
        AND (hotel.price_per_night * trip.group_size * trip.num_of_nights) <= trip.hotel_budget
        ORDER BY rating, price DESC
    '''
    cursor.execute(query, (destination))
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response