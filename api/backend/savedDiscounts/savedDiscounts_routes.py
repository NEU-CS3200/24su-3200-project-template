########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from db_connection import db

savedDiscounts = Blueprint('savedDiscounts', __name__)

@savedDiscounts.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get most popular discounts 
@savedDiscounts.route('/savedDiscounts/popular', methods=['GET'])
def get_savedDiscounts_pop():
    current_app.logger.info('GET /savedDiscounts/popular route')
    query = '''
        SELECT discountId, COUNT(*) AS saves
        FROM discount_used
        GROUP BY discountId
        ORDER BY saves DESC
        LIMIT 5
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# group saved discounts by category 
@savedDiscounts.route('/savedDiscounts/byCategory', methods=['GET'])
def get_saved_by_catgeory():
    current_app.logger.info('GET /savedDiscounts/popular route')
    query = '''
        SELECT s.category, COUNT(*) AS saves
        FROM discount_used du
        JOIN discount d ON du.discountId = d.discountId
        JOIN store s ON d.storeId = s.storeId
        GROUP BY s.category
        ORDER BY saves DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get all saved discounts
@savedDiscounts.route('/savedDiscounts', methods=['GET'])
def get_savedDiscounts():
    current_app.logger.info('GET /savedDiscounts')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT username, discountId FROM discount_used')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get saved discounts for one user, including store info
@savedDiscounts.route('/savedDiscounts/<username>', methods=['GET'])
def get_used_discounts(username):
    current_app.logger.info('GET /savedDiscounts/<username> route')
    cursor = db.get_db().cursor()
    query = '''
        SELECT d.discountId, d.code, d.percentOff, d.item, d.startDate, d.endDate,
               s.name AS storeName, s.category, s.priceRange
        FROM discount_used du
        JOIN discount d ON du.discountId = d.discountId
        JOIN store s ON d.storeId = s.storeId
        WHERE du.username = %s
    '''
    cursor.execute(query, (username,))
    row_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()
    json_data = [dict(zip(row_headers, row)) for row in theData]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# save new discounts for a user
@savedDiscounts.route('/savedDiscounts', methods=['POST'])
def add_saved_discounts():
    current_app.logger.info('POST /savedDiscounts route')
    data = request.get_json()
    query = 'INSERT INTO discount_used (username, discountId) VALUES (%s, %s)'  # !! parameterized
    cursor = db.get_db().cursor()                                                 # !!
    cursor.execute(query, (data['username'], data['discountId']))                 # !!
    db.get_db().commit()                                                          # !!

    the_response = make_response(jsonify({'message': 'saved discount added'}))    # !!
    the_response.status_code = 201                                               # !!
    the_response.mimetype = 'application/json'                                     # !!
    return the_response 

# remove a saved discount
@savedDiscounts.route('/savedDiscounts/<username>/<int:discountId>', methods=['DELETE'])
def delete_saved_discounts(username, discountId):
    current_app.logger.info('DELETE /savedDiscounts/<username>/<discountId> route')
    query = '''
        DELETE FROM discount_used
        WHERE username = %s AND discountId = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (username, discountId))
    db.get_db().commit()
    the_response = make_response(jsonify('saved discount deleted'))
    the_response.mimetype = 'application/json'
    the_response.status_code = 200
    return the_response


