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

    query = ''' SELECT professor_id, first_name, last_name, email, dept_id, office_location 
                FROM Professor WHERE professor_id = %s'''
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
