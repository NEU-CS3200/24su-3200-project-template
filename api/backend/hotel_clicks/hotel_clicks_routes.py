from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named hotel_clicks for managing click-related routes
hotel_clicks = Blueprint('hotel_clicks', __name__)

# Route to retrieve all clicks for hotels
@hotel_clicks.route('/hotel_clicks/<hotel_id>', methods=['GET'])
def get_all_hotel_clicks(hotel_id):
    current_app.logger.info(f'hotel_clicks.py: GET /hotel_clicks/{hotel_id}')
    cursor = db.get_db().cursor() 

    # Execute a SQL query to fetch the sum of clicks for the specified hotel_id
    the_query = '''SELECT SUM(click_counter) FROM hotel_clicks WHERE hotel_id = %s'''
    cursor.execute(the_query, (hotel_id,))
    
    theData = cursor.fetchone()  # Fetch the result, which should be a single value

    # Prepare the response
    the_response = make_response(jsonify({'hotel_id': hotel_id, 'total_clicks': theData[0] if theData else 0}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response