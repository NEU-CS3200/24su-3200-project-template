# ########################################################
# Admin blueprint of endpoints
# ########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from db_connection import db

admin = Blueprint('admin', __name__)

# get all admin
@admin.route('/admins', methods=['GET'])
def get_all_admins():
    current_app.logger.info('GET /admins route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT username, firstName, lastName, email, phoneNo,
               supportUser, supportClub, supportStore
        FROM admin
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for row in results:
        json_data.append(dict(zip(row_headers, row)))
    response = make_response(jsonify(json_data))
    response.mimetype = 'application/json'
    response.status_code = 200
    return response


# get specfic admin
@admin.route('/admins/<username>', methods=['GET'])
def get_admin(username):
    current_app.logger.info('GET /admins/<username> route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT username, firstName, lastName, email, phoneNo,
               supportUser, supportClub, supportStore
        FROM admin
        WHERE username = %s
    '''
    cursor.execute(query, (username, ))
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for row in results:
        json_data.append(dict(zip(row_headers, row)))
    response = make_response(jsonify(json_data))
    response.mimetype = 'application/json'
    response.status_code = 200
    return response



# add new  admin
@admin.route('/admins', methods=['POST'])
def add_admin():
    current_app.logger.info('POST /admins route')
    cursor = db.get_db().cursor()
    the_data = request.json
    query = '''
        INSERT INTO admin (username, firstName, lastName, password, email, phoneNo,
                           supportUser, supportClub, supportStore)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (
        the_data['username'],
        the_data['firstName'],
        the_data['lastName'],
        the_data['password'],
        the_data['email'],
        the_data['phoneNo'],
        the_data.get('supportUser', False),
        the_data.get('supportClub', False),
        the_data.get('supportStore'), False
    )

    cursor.execute(query, data)
    db.get_db().commit()
    the_response = make_response(jsonify({'message': 'admin added successfully'}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'  # !! Added mimetype
    return the_response

# update admin
@admin.route('/admins', methods=['PUT'])
def update_admin():
    current_app.logger.info('PUT /admins route')
    the_data = request.json
    query = '''
        UPDATE admin
        SET firstName = %s, lastName = %s, password = %s, email = %s, phoneNo = %s,
            supportUser = %s, supportClub = %s, supportStore = %s
        WHERE username = %s
    '''
    data = (
        the_data['username'],
        the_data['firstName'],
        the_data['lastName'],
        the_data['password'],
        the_data['email'],
        the_data['phoneNo'],
        the_data.get('supportUser', False),
        the_data.get('supportClub', False),
        the_data.get('supportStore'), False
    )

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    the_response = make_response(jsonify({'message': 'admin updated successfully'}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# delete admin 
@admin.route('/admins/<username>', methods=['DELETE'])
def delete_admin(username):
    current_app.logger.info('DELETE /admins/<username> route')
    query = '''DELETE FROM admin WHERE username = %s'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (username, ))
    db.get_db().commit()
    response.mimetype = 'application/json'
    response = make_response("college deleted successfully")
    response.status_code = 200
    return response