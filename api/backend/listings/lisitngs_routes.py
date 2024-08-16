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
    cursor.execute('SELECT id, BeingRented, City, ZipCode,Street,HouseNum,State,PrevPriceData,CurrPriceData,PredictedFuturePriceData,AreaId,RealtorId FROM Listings')

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
        current_app.logger.info(row)
        json_data.append(row)

    return jsonify(json_data)

@listings.route('/listings/<id>', methods=['GET'])
def get_listing_detail (id):

    query = 'SELECT id, BeingRented, City, ZipCode,Street,HouseNum,State,PrevPriceData,CurrPriceData,PredictedFuturePriceData,AreaId,RealtorId FROM Listings WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(row)
    return jsonify(json_data)
    

# get the top 5 products from the database
@listings.route('/mostExpensive')
def get_most_pop_listings():
    cursor = db.get_db().cursor()
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData,PrevPriceData,PredictedFuturePriceData
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
        json_data.append(row)

    return jsonify(json_data)

@listings.route('/listingsBeingRented', methods=['GET'])
def get_listings_Being_Rented():
    
    query = '''
        SELECT
            CASE
                WHEN BeingRented = 0 THEN 'Not Rented'
                WHEN BeingRented = 1 THEN 'Rented'
                ELSE 'Other'
            END AS Rental_Status,
            COUNT(*) AS Total_Count
        FROM
            Listings
        GROUP BY
            BeingRented;
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
        json_data.append(row)
    
    return jsonify(json_data)


@listings.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_listings():
    
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData,PrevPriceData,PredictedFuturePriceData
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
        json_data.append(row)
    
    return jsonify(json_data)


@listings.route('/tenLeastExpensive', methods=['GET'])
def get_10_least_expensive_listings():
    
    query = '''
        SELECT id, City,ZipCode,Street,HouseNum,State,CurrPriceData,PrevPriceData,PredictedFuturePriceData
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
        json_data.append(row)
    
    return jsonify(json_data)


@listings.route('/tenLeastExpensive/<State>', methods=['GET'])
def get_10_most_expensive_listings_in_state(State):
    # Prepare a parameterized SQL query to avoid SQL injection
    query = '''
        SELECT id, City, ZipCode, Street, HouseNum, State, CurrPriceData
        FROM Listings
        WHERE State = %s
        ORDER BY CurrPriceData ASC
        LIMIT 10
    '''

    # Get a cursor from the database connection
    cursor = db.get_db().cursor()

    # Execute the SQL query, passing the State parameter to fill in the placeholder %s
    cursor.execute(query, (State,))  # Make sure to pass State as a tuple

    # Fetch column headers from the cursor description
    column_headers = [x[0] for x in cursor.description]

    # Initialize a list to store JSON formatted data
    json_data = []

    # Fetch all the data from the cursor
    theData = cursor.fetchall()

    # Combine each row with the column headers to create a dictionary
    for row in theData:
        json_data.append(row)  # Use dict to format rows with headers
    
    # Return the data as JSON
    return jsonify(json_data)

@listings.route('/listings', methods=['POST'])
def add_new_listing():
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting variables from JSON and converting boolean to integer for SQL
    # Convert and validate data types
    BeingRented = bool(the_data['BeingRented'])  # Convert to boolean
    City = the_data['City']
    PrevPriceData = int(the_data['PrevPriceData'])
    ZipCode = int(the_data['ZipCode'])
    Street = the_data['Street']
    HouseNum = int(the_data['HouseNum'])
    State = the_data['State']
    CurrPriceData = int(the_data['CurrPriceData'])
    PredictedFuturePriceData = int(the_data['PredictedFuturePriceData'])
    AreaId = int(the_data['AreaId'])
    RealtorId = int(the_data['RealtorId'])
    id = int(the_data['id'])

    # Constructing the parameterized query
    query = '''
        INSERT INTO Listings 
        (BeingRented, City, PrevPriceData, ZipCode, Street, HouseNum, State, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorId,id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    '''
    # Tuple for parameters to ensure safe SQL execution
    values = (
        BeingRented, City, PrevPriceData, ZipCode, Street, HouseNum, State, CurrPriceData,
        PredictedFuturePriceData, AreaId, RealtorId,id
    )

    # Executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    
    return jsonify({"success": True, "message": "New listing added successfully"}), 201



### Get all product categories
@listings.route('/listingStates', methods = ['GET'])
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
        json_data.append(row)
    
    return jsonify(json_data)

@listings.route('/listings/<int:listing_id>', methods=['PUT'])
def update_listings(listing_id):
    listings_info = request.json
    current_app.logger.info(listings_info)

    update_parts = []
    values = []

    # Construct the query dynamically based on the provided JSON fields
    for key, value in listings_info.items():
        update_parts.append(f"{key} = %s")
        values.append(value)

    # Combine parts to form a full SQL query only if there are parts to update
    if update_parts:
        query = "UPDATE Listings SET " + ", ".join(update_parts) + " WHERE id = %s"
        values.append(listing_id)  # Ensure the listing ID is added as the last parameter

        try:
            cursor = db.get_db().cursor()
            # Make sure the number of placeholders matches the number of parameters
            cursor.execute(query, values)
            db.get_db().commit()
            return jsonify({"success": True, "message": "Listing updated successfully"}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to update listing: {e}")
            return jsonify({"success": False, "message": str(e)}), 500
    else:
        return jsonify({"success": False, "message": "No data provided for update"}), 400



@listings.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    cursor = db.get_db().cursor()
    try:
        # Execute the delete query
        query = "DELETE FROM Listings WHERE id = %s"
        cursor.execute(query, (listing_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            # No rows deleted, likely because the item did not exist
            return jsonify({"error": "Listing not found"}), 404
        
        return jsonify({"success": True, "message": "Listing deleted successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Failed to delete listing: {e}")
        return jsonify({"error": "Failed to delete listing"}), 500


@listings.route('/listingsViews', methods=['GET'])
def get_views_of_listing():
    
    query = '''
        SELECT City, ZipCode, Street, HouseNum, State, count(userid) AS `Number Of Views`
        FROM `Viewed Listing` join homeFinderTables.Listings L on L.id = `Viewed Listing`.ListingId
        GROUP BY City, ZipCode, Street, HouseNum, State
        ORDER BY `Number Of Views` DESC
        LIMIT 10;
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
        json_data.append(row)
    
    return jsonify(json_data)     



