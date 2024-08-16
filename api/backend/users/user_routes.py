########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

users = Blueprint('users', __name__)

# Get all customers from the DB
@users.route('/users', methods=['GET'])
def get_users():
    current_app.logger.info('user_routes.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('select id, FName,\
        LName, Gender, age, city from users')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        current_app.logger.info(f"Rows: {row}")
        #current_app.logger.info(f"Headers: {row_headers}")
        #combined_data = dict(zip(row_headers, row))
        #current_app.logger.info("Combined Data:", combined_data)
        #json_data.append(combined_data)
        #current_app.logger.info(combined_data)
        json_data.append(row)
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@users.route('/users', methods=['PUT'])
def update_users():
    current_app.logger.info('PUT /users route')
    users_info = request.json
    # current_app.logger.info(cust_info)
    users_id = users_info['id']
    first = users_info['FName']
    last = users_info['LName']
    city = users_info['city']

    query = 'UPDATE customers SET FName = %s, LName = %s, city = %s where id = %s'
    data = (first, last, city, users_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

# Get customer detail for customer with particular userID
@users.route('/users/<userID>', methods=['GET'])
def get_user(userID):
    current_app.logger.info('GET /users/<userID> route')
    cursor = db.get_db().cursor()
    cursor.execute('select id, FName, LName, city from users where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(row)
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response




@users.route('/usersgenders', methods=['GET'])
def usersgenders():
    current_app.logger.info('user_routes.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Gender, Count(Id) AS NumUniqueUsers FROM users \
                    GROUP BY Gender ORDER BY Count(Id) ASC;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        current_app.logger.info(f"Rows: {row}")
        #current_app.logger.info(f"Headers: {row_headers}")
        #combined_data = dict(zip(row_headers, row))
        #current_app.logger.info("Combined Data:", combined_data)
        #json_data.append(combined_data)
        #current_app.logger.info(combined_data)
        json_data.append(row)
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

