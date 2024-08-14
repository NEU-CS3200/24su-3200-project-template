########################################################
# Sample student blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

stuAvailability = Blueprint('stuAvailability', __name__)

@stuAvailability.route('/stuAvailability', methods = ['GET'])

def get_all_stuAvailability():
    current_app.logger.info('stuAvailability_routes.py: GET /stuAvailability')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT sa.availability_id, student_id, day, location, time
    FROM StudentAvailability sa JOIN Availability a ON sa.availability_id=a.availability_id
    JOIN Days d ON a.day_id=d.day_id
    JOIN Location l ON a.location_id=l.location_id
    JOIN Time t on a.time_id=t.time_id;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@stuAvailability.route('/stuAvailability', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /students route')
    student_aval = request.json
    # current_app.logger.info(cust_info)
    time = student_aval['time']
    days = student_aval['days']

    query = 'UPDATE students SET time = %s, days = %s where id = %s'
    data = (time,days)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Student updated!'