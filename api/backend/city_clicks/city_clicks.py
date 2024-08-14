
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

city_clicks = Blueprint('city_clicks/<city_name>', __name__)

# Getting city_clicks count
@city.route('/city_clicks/<city>', methods =['GET'])
def get_city_clicks():
    current_app.logger.info('city_clicks.py: GET /city_clicks')
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT COUNT(city_click_id)
        FROM city_clicks
        WHERE city = '''+str(city)
        
    cursor.execute(the_query) 
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


#ADD THIS TO rest_entry.py
# app.register_blueprint(cityclicks,    url_prefix='/cc')


