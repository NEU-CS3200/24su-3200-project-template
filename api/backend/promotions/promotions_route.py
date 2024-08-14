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
    cursor.execute('select code, name, discount_amount, terms_and_conditions from promotions')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
