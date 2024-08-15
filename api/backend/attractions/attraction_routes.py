from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

attractions = Blueprint("attractions", __name__)

# Get recommended attractions based on price and ordered by rating
@attractions.route('/rating/<max_price>', methods = ['GET'])
def get_attractions(max_price):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT attraction.price, attraction.address, attraction.name, attraction.rating
        FROM attraction JOIN trip ON trip.city_id = attraction.city_id
        WHERE attraction.price <= %s
        ORDER BY rating DESC
    '''
    cursor.execute(the_query, (max_price))

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# User can give the hotel a rating, [REMOVE???]
@attractions.route('/give_rating', methods = ['POST'])
def post_rating():
    the_data = request.json
    current_app.logger.info(the_data) 

    rating = the_data['rating']
    hotel_id = the_data['id']

    # how to ensure is inserted/ connected to the correct hotel?
    # have to insert in a new table for hotel containing its new rating from the user?
    query = '''
        INSERT INTO hotel (id, room_type, amenities, price_per_night, email, name, rating, city_id)
            VALUES (
    '''
    query += rating +')'
    query += 'WHERE hotel.id = ' + hotel_id

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
