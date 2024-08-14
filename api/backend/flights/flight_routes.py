from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

flights = Blueprint("flights", __name__)

# Gets all the flights that fit under a certain price range
@flights.route('/price_range/<max_price>/<min_price>)', methods = ['GET'])
def price_range(max_price, min_price):
    current_app.logger.info('flight_routes.py: GET based on budget')
    cursor = db.get_db().cursor()
    the_query = '''
        Select airline_name, duration, price 
        From flights
        Where max_price >
    '''
    cursor.execute(the_query)

    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
