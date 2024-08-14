from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

flights = Blueprint("flights", __name__)

# Gets all the flights that fit under a certain price range
@flights.route('/price/<max_price>)', methods = ['GET'])
def price_range(max_price):
    current_app.logger.info('flight_routes.py: GET based on budget')
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT airline_name, duration, price 
        FROM flights
        WHERE price <= %s
        ORDER BY price ASC
    '''
    cursor.execute(the_query, (max_price))

    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#     formatted_results = [dict(zip(['airline_name', 'duration', 'price'], row)) for row in results]
#     return jsonify(formatted_results)

# Based on the prefered duration of the user, returns possible flights and locations
@flights.route('/duration/<duration>', methods = ['GET'])
def duration(duration):
    current_app.logger.info('flight_routes.py: GET based on duration')
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT airline_name, duration, price, city_id
        FROM flights JOIN CITY on flights.city_id = city.id
        WHERE duration <= %s
        ORDER BY duration ASC
    '''
    cursor.execute(the_query, (duration))

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
