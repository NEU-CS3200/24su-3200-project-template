
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

city = Blueprint('city', __name__)


# Getting city 
@city.route('/city/<name>', methods =['GET'])
def get_city(name):
    #current_app.logger.info('city.py: GET /city')
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT country, rating FROM city WHERE name = %s
'''
    cursor.execute(the_query, (name,)) 
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#FROM city
#so user can put in new rating
@city.route('/city/<name>', methods=['POST'])
def add_new_city_rating(name):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['name']
    rating = the_data['rating']

    # Constructing the query
    query = 'insert into city (name, rating) ("'
    query += name + '", "'
    query += rating + '", "'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#ADD THIS TO rest_entry.py
# app.register_blueprint(city,    url_prefix='/c')
#comment out other c for /customers since there will be two c's; also just an example
