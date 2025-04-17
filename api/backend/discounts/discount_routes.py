########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from db_connection import db
# from backend.ml_models.model01 import predict


discounts = Blueprint('discounts', __name__)

# add a new discount to the DB
@discounts.route('/discounts', methods=['POST'])
def add_discount():
    current_app.logger.info('POST /discounts route')
    data = request.get_json()

    required_fields = ['storeId', 'code', 'percentOff', 'item', 'startDate',
                       'endDate', 'ageRestricted', 'minPurchase', 'bdayDiscount']


    if not all(field in data for field in required_fields):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    try:

        query = '''
            INSERT INTO discount (storeId, code, percentOff, item, startDate,
                                  endDate, ageRestricted, minPurchase, bdayDiscount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            data['storeId'],
            data['code'],
            data['percentOff'],
            data['item'],
            data['startDate'],
            data['endDate'],
            data['ageRestricted'],
            data['minPurchase'],
            data['bdayDiscount']
        )


        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        return make_response(jsonify({'message': 'Discount added successfully'}), 201)

    except Exception as e:
        current_app.logger.error(f"Error inserting discount: {e}")
        return make_response(jsonify({'error': 'Failed to add discount'}), 500)


@discounts.route('/discounts', methods=['GET'], endpoint='get_discounts_route')
def get_discounts():
    print("🔍 Flask: GET /discounts hit!")

    cursor = db.get_db().cursor()

    query = '''
        SELECT discountId, storeId, code, percentOff, item, startDate,
               endDate, ageRestricted, minPurchase, bdayDiscount
        FROM discount
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()

    if not data:
        return jsonify([])  # 👈 even if empty, send a JSON list

    json_data = [dict(zip(row_headers, row)) for row in data]
    return jsonify(json_data)

# update a discount by ID
@discounts.route('/discounts/<int:discountId>', methods=['PUT'])
def update_discount(discountId):
    current_app.logger.info('PUT /discounts/<discountId> route')
    data = request.get_json()
    query = '''
        UPDATE discount SET percentOff = %s, endDate = %s
        WHERE discountId = %s
    '''
    values = (
        data['percentOff'], 
        data['endDate'],
        discountId
    )
    cursor = db.get_db().cursor()
    cursor.execute(query,values)
    db.get_db().commit()
    return 'discount updated successfully'

# delete a discount by ID 
@discounts.route('/discounts/<int:discountId>', methods=['DELETE'])
def delete_discount(discountId):
    current_app.logger.info('DELETE /discounts/<discountId> route')
    query = '''
        DELETE FROM discount WHERE discountId = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (discountId,))
    db.get_db().commit()
    return 'discount deleted successfully'

# get list of discounts by category
@discounts.route('/discounts/categories', methods=['GET'])
def get_discount_categories():
    current_app.logger.info('GET /discounts/categories route')
    cursor = db.get_db().cursor()

    query = '''
        SELECT DISTINCT category FROM store
    '''
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
    
