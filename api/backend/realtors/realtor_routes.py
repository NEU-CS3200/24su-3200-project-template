from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


realtors = Blueprint('Realtor', __name__)

# Get all the realtors from the database
@realtors.route('/realtors', methods=['GET'])
def get_realtors():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of realtors
    cursor.execute('SELECT id, FName, LName, City FROM Realtor')

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

@realtors.route('/realtors/<id>', methods=['GET'])
def get_realtor_name (id):

    query = 'SELECT City, ZipCode, Street, HouseNum, State, RealtorId, id, Views FROM Listings WHERE RealtorId = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(row)
    return jsonify(json_data)
    


    
@realtors.route('/add_realtor', methods=['POST'])
def add_new_realtor():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    FName = the_data['FName']
    LName = the_data['LName']
    City = the_data['City']
    id = the_data['id']

    # Constructing the query
    query = '''
    INSERT INTO Realtor (FName, LName, City, id) 
    VALUES (%s, %s, %s, %s)
    '''
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
@realtors.route('/update_realtor/<id>', methods = ['PUT'])
def update_realtor():
    realtor_info = request.json
    current_app.logger.info(realtor_info)
    #Get values to change
    FName = realtor_info.get('FName')
    LName = realtor_info.get('LName')
    City = realtor_info.get('City')
    # SQL query
    query = f"""
        UPDATE Realtor
        SET FName = '{Fname}', LName = {LName}, City = {City}
        WHERE id = {id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    current_app.logger.info(f"Updated realtor with ID: {id}")
    return "Success"
@realtors.route('/delete_realtor/<id>', methods = ['DELETE'])
def delete_realtor():
    realtor_info = request.json
    current_app.logger.info(realtor_info)
    cursor = db.get_db().cursor()
    query = f"DELETE FROM Realtor WHERE id = {id}"
    cursor.execute(query)
    db.get_db().commit()
    current_app.logger.info(f"Deleted realtor with ID: {id}")
    return "Success"