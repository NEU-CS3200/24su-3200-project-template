from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

hotel = Blueprint('hotel', __name__)

# Getting hotels based on trip destination and total budget
@hotel.route('/hotel/<destination>', methods =['GET'])
def get_hotel(destination):
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    query = f'''
        Select hotel.id, hotel.room_type, hotel.amenities, hotel.price_per_night, hotel.rating, hotel.city_id, hotel.email
        FROM hotel JOIN trip ON hotel.city_id = trip.city_id
        JOIN city ON hotel.city_id = city.id
        WHERE city.name like "{destination}"
        AND (hotel.price_per_night * trip.num_of_nights) <= trip.hotel_budget
        ORDER BY rating, price_per_night DESC;
    '''
    current_app.logger.info(f'query = {query}')
    cursor.execute(query)
    
    theData = cursor.fetchall()
    current_app.logger.info(f'retVal = {theData}')
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
    