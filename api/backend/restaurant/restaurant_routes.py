
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

restaurant = Blueprint('restaurant', __name__)

# Get restaurant detail for customer with particular trip id 
#restaurant inputs id for their trip and based on the city that the trip is located in, we send back restaurant recommendations sorted by least to most expensive


@restaurant.route('/restaurant/<trip_id>', methods=['GET'])
def get_restaurant(trip_id): 
    current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    the_query = '''SELECT name, average_price, address, rating 
        FROM restaurant join city on restaurant.city_id = city.id
        join trip on trip.city_id = city.id 
        WHERE trip.id = {0} 
        ORDER BY restaurant.average_price ASC 
'''.format(trip_id)
    cursor.execute(the_query)
    #row_headers = [x[0] for x in cursor.description]
    #json_data = []
    theData = cursor.fetchall()
    #for row in theData:
       # json_data.append(dict(zip(row_headers, row)))
    #the_response = make_response(jsonify(json_data))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#FROM restaurant
@restaurant.route('/trip', methods=['POST'])
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


