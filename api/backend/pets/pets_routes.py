########################################################
# Sample pets blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

pets = Blueprint('pets', __name__)

# Get all pets from the DB
@pets.route('/pets', methods=['GET'])
def get_pets():
    current_app.logger.info('pets_routes.py: GET /pets')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT petID, name, adoption_status,\
        species, breed, birthday, age, is_alive FROM pets')

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all avilable Pets for potention adopter viewing
@pets.route('/pets/available', methods=['GET'])
def get_available_pets():
    current_app.logger.info('pets_routes.py: GET /pets/available')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT petID, name,\
        species, breed, age FROM pets WHERE is_alive = 1 AND adoption_status = 0')

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@pets.route('/pets', methods=['PUT'])
def update_pets():
    current_app.logger.info('PUT /pets route')
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


    query = 'UPDATE pets SET name = %s, adoption_status = %s, species = %s, breed = %s, birthday = %s,\
             age = %s, is_alive = %s WHERE petID = %s'
    data = (petID, name, status, species, breed, birthday, age, alive)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

# Get pet detail for a pet with particular petID
@pets.route('/pets/<petID>', methods=['GET'])
def get_pet(petID):
    current_app.logger.info('GET /pets/<petID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT name, adoption_status, species, breed, birthday, age, is_alive FROM pets WHERE petID = ' + str(petID))

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response