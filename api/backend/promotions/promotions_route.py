from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

promotions = Blueprint('promotions', __name__)

# Gets all promotions from getawayguru
@promotions.route('/promotions', methods =['GET'])
def get_promotions():
    current_app.logger.info('promotions_routes.py: GET /promotions')
    cursor = db.get_db().cursor()
    cursor.execute('select code, name, discount_amount, terms_and_conditions, marketing_campaign_id from promotions')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Adding a new promotion
@promotions.route('/promotions', methods=['POST'])
def add_new_promotion():
    the_data = request.json
    current_app.logger.info(the_data)
    code = the_data['code']
    name = the_data['name']
    discount_amount = the_data['discount_amount']
    terms_and_conditions = the_data['terms_and_conditions']
    marketing_campaign_id = the_data['marketing_campaign_id']
    

    query = 'insert into employee (code, name, discount_amount, terms_and_conditions, marketing_campaign_id) values("'
    query += code + '", "'
    query += name + '", "'
    query += discount_amount + '", "' 
    query += terms_and_conditions + '", "'
    query += marketing_campaign_id + ')'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db.commit()
    return 'Success'

# Updates a promotion
@employees.route ('/promotion', methods = ['PUT'])
def update_promotion():
    promotion_info = request.json
    code = promotion_info['code']
    name = promotion_info['name']
    discount_amount = promotion_info['discount_amount']
    terms_and_conditions = promotion_info['terms_and_conditions']
    marketing_campaign_id = promotion_info['marketing_campaign_id']

    query = 'UPDATE promotions SET name = %s, discount_amount = %s, terms_and_conditions = %s, marketing_campaign_id = %s, where code = %s'
    data = (name, discount_amount, terms_and_conditions, marketing_campaign_id, code)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Promotion Updated '

