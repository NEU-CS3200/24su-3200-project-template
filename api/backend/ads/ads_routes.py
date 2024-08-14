from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

ads = Blueprint('ads', __name__)

# Get all the ads type and description from a marketing campaign 
@ads.route('/ads', methods =['GET'])
def get_ads():
    current_app.logger.info('customer_routes.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('select types, description from ads')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response