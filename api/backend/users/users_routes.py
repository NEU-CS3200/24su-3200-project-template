########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from db_connection import db

users = Blueprint('users', __name__)

@users.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Get a single users information from the DB
@users.route('/users/<username>', methods=['GET'])
def get_user(username):
    current_app.logger.info(' GET /users/<username> route')
    cursor = db.get_db().cursor()
    query = ('''SELECT username, firstName, lastName, password, college, email,
               phoneNo, birthdate, age, discountsUsed
        FROM user
        WHERE username = %s''')
    cursor.execute(query, (username,))
    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
    return make_response(jsonify(json_data), 200)

# get all users and their info 
@users.route('/users', methods=['GET'])
def get_all_users():
    current_app.logger.info(' GET /users route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT username, firstName, lastName, password, college, email,
               phoneNo, birthdate, age, discountsUsed
        FROM user
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
    return make_response(jsonify(json_data), 200)

@users.route('/users', methods=['POST'])
def add_new_user():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = '''
        INSERT INTO user (username, firstName, lastName, password, college,
                          email, phoneNo, birthdate, age, discountsUsed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (
        the_data['username'],
        the_data['firstName'],
        the_data['lastName'],
        the_data['password'],
        the_data['college'],
        the_data['email'],
        the_data['phoneNo'],
        the_data['birthdate'],
        the_data['age'],
        the_data['discountsUsed']
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response("user added successfully", 201)

@users.route('/users', methods=['PUT'])
def update_user():
    current_app.logger.info('PUT /users route')
    user_info = request.json

    query = '''
        UPDATE user
        SET firstName = %s, lastName = %s, password = %s,
            college = %s, email = %s, phoneNo = %s,
            birthdate = %s, age = %s, discountsUsed = %s
        WHERE username = %s
    '''
    data = (
        user_info['firstName'],
        user_info['lastName'],
        user_info['password'],
        user_info['college'],
        user_info['email'],
        user_info['phoneNo'],
        user_info['birthdate'],
        user_info['age'],
        user_info['discountsUsed'],
        user_info['username']
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return "user updated successfully"

# delete a user
@users.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    current_app.logger.info('DELETE /users/<username> route')

    query = '''DELETE FROM user WHERE username = %s'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (username,))
    db.get_db().commit()
    response = make_response('user deleted succesfully')
    response.status_code = 200
    return response