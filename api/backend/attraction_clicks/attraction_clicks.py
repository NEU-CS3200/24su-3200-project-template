from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named attraction_clicks for managing click-related routes
attraction_clicks = Blueprint('attraction_clicks', __name__)

# Route to retrieve all clicks for attractions
@attraction_clicks.route('/attraction_clicks/alldata', methods=['GET'])
def get_all_attraction_clicks():
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch all records from the attraction_clicks table
    cursor.execute('SELECT attraction_id, SUM(click_counter) AS total_clicks FROM attraction_clicks GROUP BY attraction_id')
    
    clicks_data = cursor.fetchall()

    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'  
    return the_response