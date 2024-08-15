########################################################
# Sample availability blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
#from app.src.pages.prediction_11 import submit_taForm
#from backend.ml_models.model01 import predict

availability = Blueprint('availability', __name__)

@availability.route('/availability', methods=['POST'])
def add_new_avail():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    time = the_data['time_id']
    day = the_data['day_id']

    # Constructing the query
    query = 'INSERT INTO Availability(day_id, time_id) VALUES ("'
    query += day + '", "' + time + '")'
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'