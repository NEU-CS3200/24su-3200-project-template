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
        Select hotel.id, hotel.room_type, hotel.amenities, hotel.price_per_night, trip.num_of_nights, trip.hotel_budget, hotel.rating, hotel.city_id, hotel.email
        FROM hotel JOIN trip ON hotel.city_id = trip.city_id
        JOIN city ON hotel.city_id = city.id
        WHERE city.name like "{destination}"
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

@hotel.route('/add_review', methods=['POST'])
def add_new_hotel_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    rating = the_data['rating']


    # Constructing the query
    query = 'insert your rating for the hotel ("'
    query += rating + '", "'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

    