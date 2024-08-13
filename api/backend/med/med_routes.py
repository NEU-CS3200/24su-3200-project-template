########################################################
# Sample medical history blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

med = Blueprint('med', __name__)

# Get all medical history entries from a specific pet
@med.route('/med/<petID>', methods=['GET'])
def med_pets(petID):
    current_app.logger.info('med_routes.py: GET /med')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT petID, entryNumber, entry, date FROM medical_records WHERE petID = ' + str(petID))

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new entry in the pet medical record
@med.route('/med/<petID>', methods=['POST'])
def add_entry(petID):
    current_app.logger.info('POST /med route')
    med_info = request.json
    entry = med_info['entry']
    date = med_info['date']

    query = 'INSERT INTO medical_records (entry, petID, date) VALUES (%s, %s, %s)'
    data = (entry, petID, date)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'medical entry added!'  

