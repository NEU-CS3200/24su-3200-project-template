from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named hotel_clicks for managing click-related routes
hotel_clicks = Blueprint('hotel_clicks', __name__)

# Route to retrieve all clicks for hotels
@hotel_clicks.route('/hotel_clicks/alldata', methods=['GET'])
def get_all_hotel_clicks():
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch all records from the hotel_clicks table
    cursor.execute('SELECT hotel_id, click_counter, user_id, clicked_at, hotel_click_id FROM hotel_clicks')
    
    clicks_data = cursor.fetchall()

    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'  
    return the_response  