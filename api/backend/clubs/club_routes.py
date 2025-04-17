# ########################################################
# Club blueprint of endpoints
# ########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
# from db_connection.connector import db
from db_connection import db

clubs = Blueprint('clubs', __name__)

# get all clubs
@clubs.route('/clubs', methods=['GET'])
def get_all_clubs():
    current_app.logger.info('GET /clubs route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT clubId, name, college, numberOfUsers
        FROM club '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = [dict(zip(row_headers, row)) for row in results]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get details for a specfic club
@clubs.route('/clubs/<int:clubId>', methods=['GET'])
def get_club(clubId):
    current_app.logger.info('/clubs/<clubId> route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT clubId, name, college, numberOfUsers
        FROM club
        WHERE clubId = %s
    '''
    cursor.execute(query, (clubId,))
    row_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()
    json_data = [dict(zip(row_headers, row)) for row in theData]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# add a new club
@clubs.route('/clubs', methods=['POST'])
def add_club():
    current_app.logger.info('/clubs route')
    data = request.get_json()
    query = '''
        INSERT INTO club (name, college, numberOfUsers)
        VALUES (%s, %s, %s)
    '''
    values = (
        data['name'],
        data['college'],
        data.get('numberOfUsers', 0)
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    the_response = make_response(jsonify({'message': 'club added successfully'}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response


# update a club
@clubs.route('/clubs/<int:clubId>', methods=['PUT'])
def update_club(clubId):
    current_app.logger.info('PUT /clubs<int:clubId> route')
    data = request.get_json()
    query = '''
        UPDATE club
        SET name = %s, college = %s, numberOfUsers = %s
        WHERE clubId = %s
    '''
    values = (
        data['name'],
        data['college'],
        data.get('numberOfUsers'),
        clubId
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    if cursor.rowcount == 0:
        return make_response("No club found to update", 404)
    return make_response("club updated successfully", 200)


# delete a club
@clubs.route('/clubs/<int:clubId>', methods=['DELETE'])
def delete_club(clubId):
    current_app.logger.info('DELETE /clubs<int:clubId> route')
    query = '''
        DELETE FROM club WHERE clubId = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (clubId, ))
    db.get_db().commit()
    if cursor.rowcount == 0:
        return make_response("no club found to delete", 404)
    return make_response("club deleted successfully", 200)

# get all users in a club
@clubs.route('/clubs/<int:clubId>/users', methods=['GET'])
def get_users_in_club(clubId):
    current_app.logger.info('GET /clubs/<clubId>/users route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT u.username, u.firstName, u.lastName, u.email
        FROM user_club uc
        JOIN user u ON uc.username = u.username
        WHERE uc.clubId = %s
    '''
    cursor.execute(query, (clubId,))
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = [dict(zip(row_headers, row)) for row in results]
    return make_response(jsonify(json_data), 200)

# add user to a club
@clubs.route('/clubs/<int:clubId>/users', methods=['POST'])
def add_user_to_club(clubId):
    current_app.logger.info('POST /clubs/<clubId>/users route')
    data = request.get_json()
    username = data['username']
    query = '''
        INSERT INTO user_club (username, clubId)
        VALUES (%s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (username, clubId, ))
    db.get_db().commit()
    return make_response("user added to club successfully", 201)

# remove user from a club
@clubs.route('/clubs/<int:clubId>/users/<username>', methods=['DELETE'])
def remove_user_from_club(clubId, username):
    current_app.logger.info('DELETE /clubs/<int:clubId>/users/<username> route')
    query = '''
        DELETE FROM user_club
        WHERE clubId = %s AND username = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (clubId, username))
    db.get_db().commit()
    return make_response("user removed from club successfully", 200)


