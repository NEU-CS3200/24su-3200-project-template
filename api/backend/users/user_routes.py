from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

users = Blueprint("users", __name__)

# retrieve user information
@users.route('/users', methods =['GET'])
def get_users():
    current_app.logger.info('users_route.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT username, address FROM users')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# create a new user account with user information
@users.route('/create_account', methods = ['POST'])
def create_account():
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['username']
    address = the_data['address']
    email = the_data['email']

    query = 'INSERT into users (email, address, username)'
    query += email + ", "
    query += address + ", "
    query += name + ")"
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Update the users account details
@users.route('/update_account', methods = ['PUT'])
def update_account():
    current_app.logger.info('PUT /users route')
    user_info = request.json

    user_id = user_info['id']
    email = user_info['email']
    address = the_data['address']
    username = the_data['username']

    query = 'UPDATE customers SET email = %s, address = %s, username = %s where id = %s'
    data = (email, address, username, user_id)x
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'