from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

ads = Blueprint('ads', __name__)

# Get all the ads informations from a marketing campaign 
@ads.route('/ads', methods =['GET'])
def get_ads():
    current_app.logger.info('ads_routes.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('select id, terms_and_conditions, description, types, description from ads')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Adding a new ad 
@employees.route('/ads', methods=['POST'])
def add_new_employee():
    the_data = request.json
    current_app.logger.info(the_data)
    id = the_data['id']
    description = the_data['description']
    types = the_data['types']
    terms_and_conditions = the_data['terms_and_conditions']
    budget = the_data['budget']

    query = 'insert into ads (id, description, types, terms_and_conditions, budget) values("'
    query += id + '", "'
    query += description + '", "'
    query += types + '", "' 
    query += terms_and_conditions + '", "'
    query += budget + ')'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db.commit()
    return 'Success'