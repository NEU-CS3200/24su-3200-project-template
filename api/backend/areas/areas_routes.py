from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


areas = Blueprint('area', __name__)

# Get all the areas from the database
@areas.route('/areas', methods=['GET'])
def get_areas():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of areas
    cursor.execute('SELECT id, name FROM area')

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
        json_data.append(row)

    return jsonify(json_data)

@areas.route('/areas/<id>', methods=['GET'])
def get_area_name (id):

    query = 'SELECT id, name FROM area WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(row)
    return jsonify(json_data)
    
@areas.route('/areasname/<name>', methods=['GET'])
def get_area_home(name):

    query = 'SELECT id, name, AveragePrice, SchoolQuality FROM area WHERE name = "' + str(name + '"')
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(row)
    return jsonify(json_data)

    
@areas.route('/add_area', methods=['POST'])
def add_new_area():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['name']
    avg_price = the_data['AveragePrice']
    school_quality = the_data['SchoolQuality']
    id = the_data['id']

    # Constructing the query
    query = '''
    INSERT INTO area (name, AveragePrice, SchoolQuality, id) 
    VALUES (%s, %s, %s, %s)
    '''
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
@areas.route('/update_area/<id>', methods = ['PUT'])
def update_area():
    area_info = request.json
    current_app.logger.info(area_info)
    #Get values to change
    name = area_info.get('name')
    avg_price = area_info.get('AveragePrice')
    school_quality = area_info.get('SchoolQuality')
    # SQL query
    query = f"""
        UPDATE area
        SET name = '{name}', AveragePrice = {avg_price}, SchoolQuality = {school_quality}
        WHERE id = {id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    current_app.logger.info(f"Updated area with ID: {id}")
    return "Success"
@areas.route('/delete_area/<id>', methods = ['DELETE'])
def delete_area():
    area_info = request.json
    current_app.logger.info(area_info)
    cursor = db.get_db().cursor()
    query = f"DELETE FROM area WHERE id = {id}"
    cursor.execute(query)
    db.get_db().commit()
    current_app.logger.info(f"Deleted area with ID: {id}")
    return "Success"

