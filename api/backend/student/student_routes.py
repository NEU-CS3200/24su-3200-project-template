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

# this is the route to update a student's major 
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

# this route is to find students in the same section & live on campus 
@students.route('/students/<email>/on-campus', methods=['GET'])
def find_oc(email):
    current_app.logger.info('student_routes.py: GET /students/<email>/on-campus')

    # Establish database connection
    connection = db.get_db()
    cursor = connection.cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT student_id
                FROM Student
                WHERE email=%s'''
    cursor.execute(query_id, (email))
    theData = cursor.fetchone()

    if theData:
        student_id = theData['student_id']
        
        query_sec = '''SELECT c.course_name, ss.semester_year, ss.section_num, s.first_name, s.last_name, s.email, s.on_campus
                    FROM StudentSection ss
                    JOIN Student s ON ss.student_id = s.student_id
                    JOIN Class c ON ss.course_id = c.course_id
                    WHERE ss.section_num IN (SELECT section_num
                    FROM StudentSection WHERE student_id = %s)
                    AND ss.semester_year IN (SELECT semester_year
                    FROM StudentSection WHERE student_id = %s)
                    AND ss.course_id IN (SELECT course_id 
                    FROM StudentSection WHERE student_id = %s)
                    AND s.on_campus IS TRUE;'''
        
        cursor.execute(query_sec, (student_id, student_id, student_id))
        theData = cursor.fetchall()
        the_response = make_response(theData)
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response


'''' @students.route('/avail/<email>', methods=['POST'])
def update_avail():
    current_app.logger.info('POST /students route')
    student_info = request.json
    # current_app.logger.info(cust_info)
    f_name = student_info['f_name']
    l_name = student_info['l_name']
    email = student_info['email']
    major = student_info['major']
    interests = student_info['interests']
    year = student_info['year']
    dorm = student_info['dorm']

    query = 'INSERT INTO students SET f_name = %s, l_name = %s, email = %s, major = %s, interests = %s, year = %s, dorm=%s where id = %s'
    data = (f_name,l_name,email,major,interests,year,dorm)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Student Inserted!'

@students.route('/students', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /students route')
    student_info = request.json
    # current_app.logger.info(cust_info)
    f_name = student_info['f_name']
    l_name = student_info['l_name']
    email = student_info['email']
    major = student_info['major']
    interests = student_info['interests']
    year = student_info['year']
    dorm = student_info['dorm']

    query = 'UPDATE students SET f_name = %s, l_name = %s, email = %s, major = %s, interests = %s, year = %s, dorm=%s where id = %s'
    data = (f_name,l_name,email,major,interests,year,dorm)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Student updated!' '''

