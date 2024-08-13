########################################################
# Sample adoptions blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

adoptions = Blueprint('adoptions', __name__)

# Get all adoption info
@adoptions.route('/adoptions', methods=['GET'])
def med_pets():
    current_app.logger.info('adoptions_routes.py: GET /med')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT name, petID, firstName, lastName, adopterID, email, phone, adoption_date,\
                    adoptionID FROM adopters NATURAL JOIN adoptions NATURAL JOIN pets')

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


