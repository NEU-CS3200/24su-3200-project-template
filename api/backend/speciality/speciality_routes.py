########################################################
# Sample student blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

speciality = Blueprint('speciality', __name__)

@speciality.route('/speciality/', methods = ['GET'])

def get_all_students():
    current_app.logger.info('speciality_routes.py: GET /speciality')
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT speciality
    FROM Speciality;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



