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
        Select hotel.id, hotel.room_type, hotel.amenities, hotel.price_per_night, hotel.rating, hotel.city_id 
        FROM hotel JOIN trip ON hotel.city_id = trip.city_id
        JOIN city ON hotel.city_id = city.id
        WHERE city.name = %s
        AND (hotel.price_per_night * trip.group_size * trip.num_of_nights) <= trip.hotel_budget
        ORDER BY rating, price_per_night DESC
    '''
    cursor.execute(query, (destination))
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response