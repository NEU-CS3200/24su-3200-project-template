# ########################################################
# Colleges blueprint of endpoints
# ########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from db_connection import db

colleges = Blueprint('colleges', __name__)

# get all colleges
@colleges.route('/colleges', methods=['GET'])
def get_all_colleges():
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            collegeName,
            location,
            noOfStores,
            noOfUsers,
            domain
        FROM college
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for row in results:
        json_data.append(dict(zip(row_headers, row)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    return response

# get a specfic college, by name

@colleges.route('/colleges/<collegeName>', methods=['GET'])
def get_college(collegeName):
    current_app.logger.info('GET /colleges/<collegeName> route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            collegeName,
            location,
            noOfStores,
            noOfUsers,
            domain
        FROM college
        WHERE collegeName = %s
    '''
    cursor.execute(query, (collegeName,))
    row_headers = [x[0] for x in cursor.description]
    the_data = cursor.fetchall()
    json_data = []
    for row in the_data:
        json_data.append(dict(zip(row_headers, row)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    return response

# add a new college
@colleges.route('/colleges', methods=['POST'])
def add_college():
    current_app.logger.info('POST /colleges route')
    the_data = request.json
    collegeName = the_data['collegeName']
    location = the_data['location']
    noOfStores = the_data['noOfStores']
    noOfUsers = the_data['noOfUsers']
    domain = the_data['domain']

    query = '''
        INSERT INTO college (collegeName, location, 
                             noOfStores, noOfUsers, domain)
        VALUES (%s, %s, %s, %s, %s)
    '''
    data = (collegeName, location, noOfStores, noOfUsers, domain)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    response = make_response("college added successfully")
    response.status_code = 201
    return response


# update a college
@colleges.route('/colleges', methods=['PUT'])
def update_college():
    current_app.logger.info('PUT /colleges route')
    the_data = request.json
    collegeName = the_data['collegeName']
    location = the_data['location']
    noOfStores = the_data['noOfStores']
    noOfUsers = the_data['noOfUsers']
    domain = the_data['domain']

    query = '''
        UPDATE college
        SET location = %s,
            noOfStores = %s,
            noOfUsers = %s,
            domain = %s
        WHERE collegeName = %s
    '''
    data = (location, noOfStores, noOfUsers, domain, collegeName)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    response = make_response("college updated successfully")
    response.status_code = 200
    return response

# delete a college by name
@colleges.route('/colleges/<collegeName>', methods=['DELETE'])
def delete_college(collegeName):
    current_app.logger.info('DELETE /colleges/<collegeName> route')

    query = '''
        DELETE FROM college WHERE collegeName = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (collegeName, ))
    db.get_db().commit()
    response = make_response("college deleted successfully")
    response.status_code = 200
    return response