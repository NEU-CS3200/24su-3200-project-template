########################################################
# Sample student blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

students = Blueprint('students', __name__)

@students.route('/students/<speciality>', methods = ['POST','GET'])

def get_all_students(speciality):
    current_app.logger.info('student_routes.py: GET /students')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT email,first_name,last_name
    FROM Student s
    JOIN StudentSpeciality ss
    ON s.student_id = ss.student_id
    JOIN Speciality sp
    ON sp.specialty_id = ss.specialty_id
    WHERE speciality = %s;
    '''
    cursor.execute(the_query,(speciality))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



