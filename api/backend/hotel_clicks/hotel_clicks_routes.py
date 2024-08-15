from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named hotel_clicks for managing click-related routes
hotel_clicks = Blueprint('hotel_clicks', __name__)

# Route to retrieve the total clicks for a specific hotel
@hotel_clicks.route('/hotel_clicks/<hotel_id>', methods=['GET'])
def get_hotel_clicks(hotel_id):
    current_app.logger.info(f'hotel_clicks.py: GET /hotel_clicks/{hotel_id}')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the specified hotel_id
    the_query = '''SELECT SUM(click_counter) AS total_clicks FROM hotel_clicks WHERE hotel_id = %s'''
    cursor.execute(the_query, (hotel_id,))

    # Fetch the result, which should be a single value
    clicks_data = cursor.fetchone()

    # Prepare the response
    the_response = make_response(clicks_data)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Route to retrieve the top five hotels with most clickss
@hotel_clicks.route('/top_hotel_clicks', methods=['GET'])
def get_top_hotel_clicks():
    current_app.logger.info(f'hotel_clicks.py: GET /top_hotel_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the specified hotel_id
    the_query = '''SELECT hotel_id, COUNT(hotel_id) as total_clicks
        FROM hotel_clicks
        GROUP BY hotel_id
        ORDER BY total_clicks DESC
        LIMIT 5;'''
    cursor.execute(the_query)

    # Fetch the result, which should be a single value
    clicks_data = cursor.fetchall()

    # Prepare the response
    the_response = make_response(jsonify(clicks_data))  # jsonify converts list to JSON
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
