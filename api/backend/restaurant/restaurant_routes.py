
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from urllib.parse import unquote

restaurant = Blueprint('restaurant', __name__)

# Get restaurant detail for customer with particular trip id 
#restaurant inputs id for their trip and based on the city that the trip is located in, we send back restaurant recommendations sorted by least to most expensive


@restaurant.route('/restaurant/<trip_id>', methods=['GET'])
def get_restaurant(trip_id): 
    #current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    the_query = '''SELECT r.name, r.average_price, r.address, r.rating 
           FROM restaurant r JOIN city c ON r.city_id = c.id
           JOIN trip t ON t.city_id = c.id 
           WHERE t.id = %s
           ORDER BY r.average_price ASC'''
    cursor.execute(the_query, (trip_id,))

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get a restaurant given a cuisine type
@restaurant.route('/restaurant_cuisine/<cuisine>/<city_name>', methods=['GET'])
def get_restaurant_name(cuisine, city_name): 
    cursor = db.get_db().cursor()
    the_query = f'''SELECT r.name, r.average_price, r.address, r.rating 
           FROM restaurant r join city c on r.city_id = c.id
           WHERE r.cuisine_type = "{unquote(cuisine)}" and c.name = "{unquote(city_name)}"
           ORDER BY average_price ASC'''
    cursor.execute(the_query)

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@restaurant.route('/cuisine/<city_name>', methods =['GET'])
def get_cuisine(city_name):
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    the_query = f'''SELECT restaurant.id, restaurant.cuisine_type
        FROM restaurant JOIN city on restaurant.city_id = city.id
        WHERE city.name = "{unquote(city_name)}"
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    restaurants_dict = {restaurant['cuisine_type']: restaurant['id'] for restaurant in theData}

    return jsonify(restaurants_dict)

#Get a restaurant given a rating 
@restaurant.route('/restaurant_rating/<rating>/<city_name>', methods=['GET'])
def get_restaurant_rating(rating, city_name): 
    #current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    the_query = f'''SELECT r.name, r.average_price, r.address, r.rating 
           FROM restaurant r join city c on r.city_id = c.id
           WHERE r.rating >= {rating} and c.name = "{unquote(city_name)}"
           ORDER BY average_price ASC'''
    cursor.execute(the_query)

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@restaurant.route('/restaurant', methods=['POST'])
def add_new_restaurant_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    rating = the_data['rating']


    # Constructing the query
    query = 'insert your rating for the restaurant ("'
    query += rating + '", "'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


#ADD THIS TO rest_entry.py
# app.register_blueprint(restaurant,    url_prefix='/r')


