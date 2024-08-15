########################################################
# Sample professors blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


professors = Blueprint('professors', __name__)

# Get all the professors from the database
@professors.route('/professors', methods=['GET'])
def get_professors():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT professor_id, first_name, last_name, dept_id, office_location FROM Professor')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@professors.route('/professor/<id>', methods=['GET'])
def get_professor_detail (id):

    query = ''' 
    SELECT professor_id, first_name, last_name, email, dept_id, office_location 
    FROM Professor 
    WHERE professor_id = %s
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (id))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
    

@professors.route('/professor', methods=['POST'])
def add_new_professor():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    first_name = the_data['first_name']
    last_name = the_data['last_name']
    email = the_data['email']
    dept_id = the_data['dept_id']
    office_location = the_data['office_location']

    # Constructing the query
    query = 'INSERT INTO Professor (first_name, last_name, email, dept_id, office_location) VALUES ("'
    query += first_name + '", "'
    query += last_name + '", "'
    query += email + '", '
    query += str(dept_id) + ', "'
    query += office_location + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

### Get all departments
@professors.route('/departments', methods = ['GET'])
def get_all_departments():
    query = '''
        SELECT dept_id, dept_name 
        FROM Department
        ORDER BY dept_name
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []
    # fetch all the column headers and then all the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()
    # zip headers and data together into dictionary and then append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

@professors.route('/professor', methods = ['PUT'])
def update_professor():
    professor_info = request.json
    current_app.logger.info(professor_info)

    # extracting the variables
    professor_id = professor_info['professor_id']
    first_name = professor_info.get('first_name', '')
    last_name = professor_info.get('last_name', '')
    email = professor_info.get('email', '')
    dept_id = professor_info.get('dept_id', '')
    office_location = professor_info.get('office_location', '')

    # Constructing the update query
    query = f'UPDATE Professor SET first_name="{first_name}", last_name="{last_name}", email="{email}", dept_id={dept_id}, office_location="{office_location}" WHERE professor_id={professor_id}'
    current_app.logger.info(query)


    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


# Updated route for updating group details
@professors.route('/professors/<int:professor_id>/sections/<int:section_num>/groups/<int:group_id>', methods=['PUT'])
def update_group(professor_id, section_num, group_id):
    cursor = db.get_db().cursor()
    group_data = request.json

    group_name = group_data.get('group_name')
    ta_id = group_data.get('ta_id')

    # Check if the professor is assigned to this section
    check_query = '''
    SELECT 1 FROM Section 
    WHERE section_num = %s AND professor_id = %s
    '''
    cursor.execute(check_query, (section_num, professor_id))
    if cursor.fetchone() is None:
        return jsonify({"error": "Unauthorized: You cannot update groups in another professor's section."}), 403

    query = '''
    UPDATE `Group`
    SET group_name = %s, ta_id = %s
    WHERE group_id = %s AND section_num = %s
    AND EXISTS (SELECT 1 FROM Section sec WHERE sec.section_num = %s AND sec.professor_id = %s)
    '''
    cursor.execute(query, (group_name, ta_id, group_id, section_num, section_num, professor_id))
    db.get_db().commit()

    return jsonify({"message": "Group updated successfully"}), 200

# New Route: Update student's group in a section
@professors.route('/professors/<int:professor_id>/sections/<int:section_num>/<string:semester_year>/students/<int:student_id>', methods=['PUT'])
def update_student_in_group(professor_id, section_num, semester_year, student_id):
    cursor = db.get_db().cursor()
    data = request.json

    new_group_id = data.get('group_id')

    # Check if the professor is assigned to this section
    check_query = '''
    SELECT 1 FROM Section 
    WHERE section_num = %s AND semester_year = %s AND professor_id = %s
    '''
    cursor.execute(check_query, (section_num, semester_year, professor_id))
    if cursor.fetchone() is None:
        return jsonify({"error": "Unauthorized: You cannot update students in another professor's section."}), 403


    # Update query for the student's group
    query = '''
    UPDATE Student
    SET group_id = %s
    WHERE student_id = %s
    AND EXISTS (
        SELECT 1 FROM StudentSection ss
        JOIN Section sec ON ss.section_num = sec.section_num AND ss.semester_year = sec.semester_year
        WHERE ss.student_id = %s 
        AND sec.professor_id = %s 
        AND ss.section_num = %s 
        AND ss.semester_year = %s
    )
    '''
    cursor.execute(query, (new_group_id, student_id, student_id, professor_id, section_num, semester_year))
    db.get_db().commit()

    return jsonify({"message": "Student's group updated successfully"}), 200