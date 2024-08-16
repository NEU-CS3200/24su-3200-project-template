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

# this route gets the ta's current availability and
# finds students in the same section with the same avaiability
@ta.route('/ta/<first_name>/<last_name>/<email>', methods=['POST', 'GET'])
def get_taAvail(first_name, last_name, email):
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
        
        # long select query to find students in the same section and same availability
        query_avail = '''SELECT first_name, last_name, email, group_id, d.day, t.time
                        FROM StudentSection ss JOIN Student s ON ss.student_id = s.student_id
                        JOIN StudentAvailability sa ON s.student_id=sa.student_id
                        JOIN Availability a ON sa.availability_id=a.availability_id
                        JOIN Days d ON a.day_id = d.day_id
                        JOIN Time t ON a.time_id = t.time_id
                        WHERE ss.section_num = (SELECT section_num FROM TA WHERE ta_id=%s) AND
                        ss.semester_year = (SELECT semester_year FROM TA WHERE ta_id=%s) AND
                        ss.course_id = (SELECT course_id FROM TA WHERE ta_id=%s)
                        AND sa.availability_id IN (SELECT availability_id FROM TAAvailability WHERE ta_id=%s);'''
        
        cursor.execute(query_avail, (ta_id, ta_id, ta_id, ta_id))
        avail_data = cursor.fetchall()
        the_response = make_response(jsonify(avail_data))
    else:
        # Return an error if the TA is not found
        the_response = make_response(jsonify({'error': 'No available students'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response

# this a route for ta subpage 2: Specialty 
# this shows the logged in ta what their current specialty description is 
@ta.route('/ta/<first_name>/<last_name>/<email>/special', methods=['POST', 'GET'])
def get_taSpecial(first_name, last_name, email):
    current_app.logger.info('ta_routes.py: GET /ta/<first_name>/<last_name>/<email>/special')

    # Establish database connection
    connection = db.get_db()
    cursor = connection.cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT ta_id FROM TA WHERE first_name = %s AND last_name = %s AND email = %s'''
    cursor.execute(query_id, (first_name, last_name, email))
    theData = cursor.fetchone()

    if theData:
        ta_id = theData["ta_id"]
        
        # long select query to find students in the same section and same availability
        query_special = '''SELECT speciality
                        FROM TASpecialty ts JOIN Speciality s ON ts.specialty_id = s.specialty_id
                        WHERE ta_id=%s;'''
        
        cursor.execute(query_special, (ta_id))
        special_data = cursor.fetchall()
        the_response = make_response(jsonify(special_data))
    else:
        # Return an error if the TA is not found
        the_response = make_response(jsonify({'error': 'TA NOT found'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response

# this a route for ta subpage 2: Specialty [DIFFERENT FROM get TA special ]
# want to return a list of students who may need help with a given ta's specialty 
# aka they do not have a least on of the TA's specialty 
@ta.route('/ta/<first_name>/<last_name>/<email>/students', methods=['POST', 'GET'])
def get_taStudents(first_name, last_name, email):
    current_app.logger.info('ta_routes.py: GET /ta/<first_name>/<last_name>/<email>/students')

    # Establish database connection
    connection = db.get_db()
    cursor = connection.cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT ta_id FROM TA WHERE first_name = %s AND last_name = %s AND email = %s'''
    cursor.execute(query_id, (first_name, last_name, email))
    theData = cursor.fetchone()

    if theData:
        ta_id = theData["ta_id"]
        
        # long select query to find students in the same section and same availability
        query_stu = '''SELECT DISTINCT s.first_name, s.last_name, s.email, s.group_id
                    FROM StudentSection ss JOIN Student s ON ss.student_id = s.student_id
                    JOIN StudentSpeciality sp ON s.student_id = sp.student_id
                    JOIN Speciality sl ON sp.specialty_id = sl.specialty_id
                    WHERE ss.section_num = (SELECT section_num FROM TA WHERE ta_id=%s) AND
                    ss.semester_year = (SELECT semester_year FROM TA WHERE ta_id=%s) AND
                    ss.course_id = (SELECT course_id FROM TA WHERE ta_id=%s) AND
                    sl.specialty_id NOT IN (
                    SELECT ts.specialty_id
                    FROM TASpecialty ts
                    WHERE ts.ta_id = %s)'''
        
        cursor.execute(query_stu, (ta_id, ta_id, ta_id, ta_id))
        student_data = cursor.fetchall()
        the_response = make_response(jsonify(student_data))
    else:
        # Return an error if the TA is not found
        the_response = make_response(jsonify({'error': 'No students found'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response