from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


areas = Blueprint('areas', __name__)

# Get all the areas from the database
@areas.route('/areas', methods=['GET'])
def get_areas():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of areas
    cursor.execute('SELECT id, AveragePrice, SchoolQuality, name FROM areas')

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

@areas.route('/areas/<id>', methods=['GET'])
def get_area_name (id):

    query = 'SELECT id, name FROM areas WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
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
    query = 'insert into areas (name, AveragePrice, SchoolQuality, id) values ("'
    query += name + '", "'
    query += id + '", "'
    query += str(school_quality) + '", '
    query += str(avg_price) + ')'
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

    return "Success"
@areas.route('/delete_area/<id>', methods = ['DELETE']
def delete_area():
    area_info = request.json
    current.app.logger.info(area_info)

    return "Success"

