from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from urllib.parse import unquote

attractions = Blueprint("attractions", __name__)

# Get recommended attractions based on price and ordered by rating
@attractions.route('/attraction/<city_name>/<max_price>', methods = ['GET'])
def get_attractions(city_name, max_price):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT attraction.price, attraction.address, attraction.name, attraction.rating, attraction.city_id
        FROM attraction JOIN city ON attraction.city_id = city.id
        WHERE city.name = %s 
        AND attraction.price <= %s 
        ORDER BY attraction.rating DESC
    '''
    data = (city_name, max_price)
    cursor.execute(the_query, data)

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@attractions.route('/rating/<city_name>/<rating>', methods = ['GET'])
def get_rating(city_name, rating):
    cursor = db.get_db().cursor()
    the_query = f'''
        SELECT attraction.price, attraction.address, attraction.name, attraction.rating, attraction.city_id
        FROM attraction JOIN city on attraction.city_id = city.id
        WHERE city.name = "{unquote(city_name)}" 
        AND attraction.rating >= {rating}
        ORDER BY attraction.rating DESC
    '''
    cursor.execute(the_query)

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# User can give the hotel a rating, [REMOVE???]
@attractions.route('/attraction', methods = ['POST'])
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
