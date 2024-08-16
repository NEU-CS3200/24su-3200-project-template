
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

city_clicks = Blueprint('city_clicks/<city_name>', __name__)

# Getting city_clicks count
@city_clicks.route('/city_clicks/<city>', methods =['GET'])
def get_city_clicks(city):
    current_app.logger.info('city_clicks.py: GET /city_clicks')
    cursor = db.get_db().cursor() 
    
    the_query = '''SELECT COUNT(city_click_id) FROM city_clicks WHERE city = %s'''
    cursor.execute(the_query, (city,))  # Pass city as a tuple

    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



