########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


listings = Blueprint('Listings', __name__)

# Get all the products from the database
@listings.route('/listings', methods=['GET'])
def get_listings():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT id, BeingRented, price, City, ZipCode,Street,HouseNum,State,PrevPriceData,CurPriceData,PredictedFuturePriceData,AreaId,RealtorId,Views FROM Listings')

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

@listings.route('/listings/<id>', methods=['GET'])
def get_product_detail (id):

    query = 'SELECT id, BeingRented, price, City, ZipCode,Street,HouseNum,State,PrevPriceData,CurPriceData,PredictedFuturePriceData,AreaId,RealtorId,Views FROM Listings WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
    

# get the top 5 products from the database
@listings.route('/mostExpensive')
def get_most_pop_listings():
    cursor = db.get_db().cursor()
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData
        FROM Listings
        ORDER BY CurrPriceData DESC
        LIMIT 5
    '''
    cursor.execute(query)
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


@listings.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_products():
    
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData
        FROM Listings
        ORDER BY CurrPriceData DESC
        LIMIT 10
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

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


@listings.route('/tenLeastExpensive', methods=['GET'])
def get_10_most_expensive_products():
    
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData
        FROM Listings 
        ORDER BY CurrPriceData ASC
        LIMIT 10
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

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


@listings.route('/tenLeastExpensive/<State>', methods=['GET'])
def get_10_most_expensive_products(State):
    
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData
        FROM Listings WHERE State = State 
        ORDER BY CurrPriceData ASC
        LIMIT 10
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

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

@listings.route('/listings', methods=['POST'])
def add_new_product():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['product_name']
    description = the_data['product_description']
    price = the_data['product_price']
    category = the_data['product_category']

    # Constructing the query
    query = 'insert into products (product_name, description, category, list_price) values ("'
    query += name + '", "'
    query += description + '", "'
    query += category + '", '
    query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

### Get all product categories
@listings.route('/listings', methods = ['GET'])
def get_all_states():
    query = '''
        SELECT DISTINCT State AS state
        FROM Listings
        WHERE state IS NOT NULL
        ORDER BY state
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

@listings.route('/listings', methods = ['PUT'])
def update_listings():
    listings_info = request.json
    current_app.logger.info(listings_info)

    return "Success"