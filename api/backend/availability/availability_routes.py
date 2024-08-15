########################################################
# Sample availability blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
#from app.src.pages.prediction_11 import submit_taForm
#from backend.ml_models.model01 import predict

availability = Blueprint('availability/', __name__)

@availability.route('/avail', methods = ['GET'])
def get_all_avail():
    current_app.logger.info('availability_routes.py: GET /avail')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT *
    FROM Availability;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# add to ta availability 
@availability.route('/<email>', methods=['POST'])
def add_ta_availability(email):
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting variables
    time = the_data['time']
    day = the_data['day']

    # Query to get ta_id using the inputted email
    cursor = db.get_db().cursor()
    query_ta_id = '''SELECT ta_id
                     FROM TA
                     WHERE email=%s;'''
    cursor.execute(query_ta_id, (email,))
    theData = cursor.fetchone()
    current_app.logger.info(f"ta_id fetched: {theData}")

    if not theData:
        return 'TA not found!', 404

    ta_id = theData["ta_id"]

    # Query to get availability_id using the inputted day and time
    query_availability_id = '''SELECT availability_id
                            FROM Availability a
                            WHERE day_id = (SELECT day_id FROM Days WHERE day=%s)
                            AND time_id = (SELECT time_id FROM Time WHERE time=%s);'''
    cursor.execute(query_availability_id, (day, time))
    availabilityData = cursor.fetchone()
    current_app.logger.info(f"availability_id fetched: {availabilityData}")

    if not availabilityData:
        return 'Availability not found!', 404

    availability_id = availabilityData["availability_id"]

    # Add the TA availability entry
    insert_ta_availability_query = '''INSERT INTO TAAvailability(ta_id, availability_id) 
                                      VALUES (%s, %s);'''
    cursor.execute(insert_ta_availability_query, (ta_id, availability_id))
    db.get_db().commit()
    return 'TA availability added successfully!', 201

