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
    SELECT email,first_name,group_id,last_name,major,on_campus,student_id
    FROM Student;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# # this is route to change the major of a student! 
# @students.route('/students/<first>/<last>/<email>/<major>', methods = ['PUT', 'GET'])
# def update_major():
#     current_app.logger.info('student_routes.py: GET /ta/<first_name>/<last_name>/<email>')

#     # Establish database connection
#     connection = db.get_db()
#     cursor = connection.cursor()

#     # Use parameterized query to prevent SQL injection
#     query_id = '''SELECT ta_id FROM TA WHERE first_name = %s AND last_name = %s AND email = %s'''
#     cursor.execute(query_id, (first_name, last_name, email))
#     theData = cursor.fetchone()

#     if theData:
#         ta_id = theData["ta_id"]
        
#         # long select query to find students in the same section and same availability
#         query_avail = '''SELECT first_name, last_name, email, group_id, d.day, t.time
#                         FROM StudentSection ss JOIN Student s ON ss.student_id = s.student_id
#                         JOIN StudentAvailability sa ON s.student_id=sa.student_id
#                         JOIN Availability a ON sa.availability_id=a.availability_id
#                         JOIN Days d ON a.day_id = d.day_id
#                         JOIN Time t ON a.time_id = t.time_id
#                         WHERE ss.section_num = (SELECT section_num FROM TA WHERE ta_id=%s) AND
#                         ss.semester_year = (SELECT semester_year FROM TA WHERE ta_id=%s) AND
#                         ss.course_id = (SELECT course_id FROM TA WHERE ta_id=%s)
#                         AND sa.availability_id IN (SELECT availability_id FROM TAAvailability WHERE ta_id=%s);'''
        
#         cursor.execute(query_avail, (ta_id, ta_id, ta_id, ta_id))
#         avail_data = cursor.fetchall()
#         the_response = make_response(jsonify(avail_data))
#     else:
#         # Return an error if the TA is not found
#         the_response = make_response(jsonify({'error': 'No available students'}), 404)
    
#     the_response.mimetype = 'application/json'
#     return the_response

# !!!!!!!! THIS IS THE NEW ONE 
@students.route('/students/<first_name>/<last_name>/<email>/<major>', methods=['PUT', 'GET'])
def update_major(first_name, last_name, email, major):
    current_app.logger.info('student_routes.py: GET /students/<first_name>/<last_name>/<email>/<major>')

    # Establish database connection
    connection = db.get_db()
    cursor = connection.cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT student_id
                FROM Student
                WHERE first_name = %s
                AND last_name = %s
                AND email = %s'''
    cursor.execute(query_id, (first_name, last_name, email))
    theData = cursor.fetchone()

    if theData:
        student_id = theData['student_id']
        
        query_major = '''UPDATE Student
                        SET major = %s
                        WHERE student_id=%s'''
        
        cursor.execute(query_major, (major, student_id))
        connection.commit()  # Commit the transaction
        the_response = make_response(jsonify({'success': 'major updated successfully'}))
    else:
        # Return an error if the student is not found
        the_response = make_response(jsonify({'error': 'not a student'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response



