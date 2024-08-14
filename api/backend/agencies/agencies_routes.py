########################################################
# Sample agency blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

agencies = Blueprint('agencies', __name__)

# Get all agencies from the DB
@agencies.route('/agencies', methods=['GET'])
def get_agencies():
    current_app.logger.info('agencies_routes.py: GET /agencies')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT agencyID, agencyName, phone, email, street,\
        city, state, zip FROM agencies')

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@agencies.route('/agencies', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /agencies route')
    pet_info = request.json
    # current_app.logger.info(pet_info)
    petID = pet_info['petID']
    name = pet_info['name']
    status = pet_info['adoption_status']
    species = pet_info['species']
    breed = pet_info['breed']
    birthday = pet_info['birthday']
    age = pet_info['age']
    alive = pet_info['is_alive']


    query = 'UPDATE agencies SET name = %s, adoption_status = %s, species = %s, breed = %s, birthday = %s,\
             age = %s, is_alive = %s WHERE petID = %s'
    data = (petID, name, status, species, breed, birthday, age, alive)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

@agencies.route('/petagencies', methods=['GET'])
def pet_agencies():
    current_app.logger.info('agencies_routes.py: GET /petagencies')

    cursor = db.get_db().cursor()
    theQuery = '''
      SELECT ag.agencyName, COUNT(ad.adoptionID) AS Total_Adoptions
      FROM agencies ag
        LEFT JOIN pet_agencies pa on ag.agencyID = pa.agencyID
        LEFT JOIN adoptions ad on pa.petID = ad.petID
      GROUP BY ag.agencyID
      ORDER BY Total_Adoptions
    '''
    cursor.execute(theQuery)
    theData = cursor.fetchall()

    theResponse = make_response(theData)
    theResponse.status_code = 200
    theResponse.mimetype = 'application/json'

    return theResponse

# Get pet detail for a agency with particular petID
@agencies.route('/agencies/<zip>', methods=['GET'])
def get_agency(zip):
    current_app.logger.info('GET /agencies/<zip> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT agencyID, agencyName, phone, email, street,\
        city, state, zip FROM agencies WHERE zip = ' + str(zip))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response