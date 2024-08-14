########################################################
# Sample ta blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
#from app.src.pages.prediction_11 import submit_taForm
#from backend.ml_models.model01 import predict

ta = Blueprint('ta', __name__)

@ta.route('/ta', methods = ['GET'])

def get_all_ta():
    current_app.logger.info('ta_routes.py: GET /ta')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT ta_id, first_name, last_name, email, course_name, s.section_num, s.semester_year
    FROM TA ta JOIN Section s ON ta.section_num=s.section_num
    AND ta.semester_year=s.semester_year
    AND ta.course_id=s.course_id
    JOIN Class c ON c.course_id=s.course_id;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@ta.route('/ta/<first_name>/<last_name>/<email>', methods=['POST', 'GET'])
def get_taId(first_name, last_name, email):
    current_app.logger.info('ta_routes.py: GET /ta/<first_name>/<last_name>/<email>')

    # Establish database connection
    connection = db.get_db()
    cursor = connection.cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT ta_id FROM TA WHERE first_name = %s AND last_name = %s AND email = %s'''
    cursor.execute(query_id, (first_name, last_name, email))
    theData = cursor.fetchone()

    if theData:
        ta_id = theData["ta_id"]

        query_avail = '''SELECT d.day, t.time
                         FROM TAAvailability ta
                         JOIN Availability a ON ta.availability_id = a.availability_id
                         JOIN Days d ON a.day_id = d.day_id
                         JOIN Time t ON a.time_id = t.time_id
                         WHERE ta.ta_id = %s'''
        
        cursor.execute(query_avail, (ta_id,))
        avail_data = cursor.fetchall()
        the_response = make_response(jsonify(avail_data))
    else:
        # Return an error if the TA is not found
        the_response = make_response(jsonify({'error': 'TA not found'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response

