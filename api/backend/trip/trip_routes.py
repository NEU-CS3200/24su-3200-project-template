
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

trip = Blueprint('trip', __name__)

# Getting trips
@trip.route('/trip/<id>', methods =['GET'])
def get_trip():
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    the_query = '''SELECT start_date, end_date, name, restaurant_budget, attraction_budget, num_of_nights, city_id
        FROM trip 
        WHERE id = 
'''+str(id)
    cursor.execute(the_query)
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#FROM trip
@trip.route('/trip', methods=['POST'])
def add_new_trip():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    start_date = the_data['start_date']
    end_date = the_data['end_date']
    group_size = the_data['group_size']
    name = the_data['name']
    restaurant_budget = the_data['restaurant_budget']
    attraction_budget = the_data['attraction_budget']
    hotel_budget = the_data['hotel_budget']
    num_of_nights = the_data['num_of_nights']
    city_id = the_data['city_id']

    # Constructing the query
    query = 'insert into trip (start_date, end_date, group_size, name, restaurant_budget, attraction_budget, num_of_nights, city_id) values ("'
    query += start_date + '", "'
    query += end_date + '", "'
    query += group_size + '", '
    query += name + '", '
    query += str(restaurant_budget) + ')'
    query += str(attraction_budget) + ')'
    query += str(hotel_budget) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@trip.route('/trips/<trip_name>', methods=['DELETE'])
def delete_trip(trip_name):
    trip = trip.query.filter_by(name=name)
    if trip:
        db.session.delete(trip)
        db.session.commit()
        return jsonify({'message': 'Trip deleted successfully'}), 200
    else:
        return jsonify({'error': 'Trip not found'}), 404

#ADD THIS TO rest_entry.py
# app.register_blueprint(trip,    url_prefix='/t')


