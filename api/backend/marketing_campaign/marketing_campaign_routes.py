from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

marketing_campaign = Blueprint('marketing_campaign', __name__)

# Gets all marketing campaigns from getawayguru
@marketing_campaign.route('/marketing_campaign', methods =['GET'])
def get_campaigns():
    current_app.logger.info('marketing_campaign_routes.py: GET /marketing_campaign')
    cursor = db.get_db().cursor()
    cursor.execute('select id, name, employee_id from marketing_campaign')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Adding a new marketing campaign 
@marketing_campaign.route('/add_marketing_campaign', methods=['POST'])
def add_new_campaign():
    the_data = request.json
    current_app.logger.info(the_data)
    name = the_data['name']
    employee_id = the_data['employee_id']
    discount_amount = the_data['discount_amount']
    code = the_data['code']
    description = the_data['description']
    budget = the_data['budget']
    
    query = f'''
        Insert into marketing_campaign (name, employee_id) values (
        "{name}", "{employee_id}")
    '''
    query_2 = f'''
        Insert into promotions(discount_amount, code) values(
        {discount_amount}, "{code}")
    '''

    query_3 = f'''
        Insert into ads (description, budget) values(
        "{description}", {budget})
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db.commit()
    cursor.execute(query_2)
    db.get_db.commit()
    cursor.execute(query_3)
    db.get_db.commit()
    return 'Success'

# Updates a marketing campaign 
@marketing_campaign.route ('/update_marketing_campaign', methods = ['PUT'])
def update_campaign():
    campaign_info = request.json
    name = campaign_info['name']
    employee_id = campaign_info['employee_id']

    query = 'UPDATE marketing_campaign SET name %s, employee_id = %s where id = %s'
    data = (name, employee_id, marketing_campaign_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Marketing Campaign Updated'
