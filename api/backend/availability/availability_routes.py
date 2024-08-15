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

from flask import request, jsonify, current_app

# add & delete ta_availability
@availability.route('/<email>', methods=['POST', 'DELETE'])
def manage_ta_availability(email):
    # Establish database connection
    cursor = db.get_db().cursor()

    if request.method == 'POST':
        # Handle adding TA availability
        the_data = request.json
        current_app.logger.info(the_data)

        # Extract variables
        time = the_data.get('time')
        day = the_data.get('day')

        # Query to get ta_id using the inputted email
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

    elif request.method == 'DELETE':
        # Handle deleting TA availability
        the_data = request.json
        current_app.logger.info(the_data)

        # Extract variables
        time = the_data.get('time')
        day = the_data.get('day')

        # Query to get ta_id using the inputted email
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

        # Delete the TA availability entry
        delete_ta_availability_query = '''DELETE FROM TAAvailability
                                          WHERE ta_id = %s AND availability_id = %s;'''
        cursor.execute(delete_ta_availability_query, (ta_id, availability_id))
        db.get_db().commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return 'TA availability deleted successfully!', 200
        else:
            return 'TA availability entry not found!', 404


@availability.route('/avail/<email>', methods = ['GET'])
# Showing the TA user their current availabilities 
def get_ta_avail(email):
    current_app.logger.info('availability_routes.py: GET /TA/avail')
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
    # Query to get availabilities given a ta's id 
    the_query = '''SELECT day, time
                FROM TAAvailability ta JOIN Availability a ON ta.availability_id=a.availability_id
                JOIN Days d ON a.day_id = d.day_id
                JOIN Time t ON a.time_id = t.time_id
                WHERE ta_id=%s;'''
    cursor.execute(the_query, (ta_id))
    availData = cursor.fetchall()
    the_response = make_response(availData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


