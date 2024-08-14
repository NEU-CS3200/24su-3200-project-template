########################################################
# Sample student blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

students = Blueprint('students', __name__)

@students.route('/students', methods = ['GET'])

def get_all_students():
    current_app.logger.info('student_routes.py: GET /students')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT student_id, first_name, last_name, email, major, year, on_campus, group_id
    FROM Student;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@students.route('/students', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /students route')
    cust_info = request.json
    # current_app.logger.info(cust_info)
    f_name = data['f_name']
    l_name = data['l_name']
    email = ['email']
    major = ['major']
    interests = ['interests']
    year = data['year']
    dorm = data['dorm']

    query = 'UPDATE students SET f_name = %s, l_name = %s, email = %s, major = %s, interests = %s, year = %s, dorm=%s where id = %s'
    data = (f_name,l_name,email,major,interests,year,dorm)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Student updated!'