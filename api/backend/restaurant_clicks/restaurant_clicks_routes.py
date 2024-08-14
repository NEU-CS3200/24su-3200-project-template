from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named restaurant clicks for managing click-related routes
restaurant_clicks = Blueprint('restaurant_clicks', __name__)

# Route to retrieve all clicks for restaurants
@restaurant_clicks.route('/restaurant_clicks/alldata', methods=['GET'])
def get_all_restaurant_clicks():
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch all records from the restaurant_clicks table
    cursor.execute('SELECT restaurant_id, SUM(click_counter) AS total_clicks FROM restaurant_clicks GROUP BY restaurant_id')
    
    clicks_data = cursor.fetchall()

    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response