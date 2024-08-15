from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named hotel_clicks for managing click-related routes
hotel_clicks = Blueprint('hotel_clicks', __name__)

# Route to retrieve the total clicks for the top 5 most clicked hotels
@hotel_clicks.route('/hotel_clicks', methods=['GET'])
def get_hotel_clicks():
    current_app.logger.info(f'hotel_clicks.py: GET /hotel_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks of the top 5 most clicked hotels
    the_query = '''SELECT name, SUM(click_counter) AS total_clicks 
    FROM hotel_clicks join hotel ON hotel.id = hotel_clicks.hotel_id
    GROUP BY name
    ORDER BY total_clicks desc
    Limit 5'''
    cursor.execute(the_query)

    # Fetch the result, which should be a single value
    clicks_data = cursor.fetchone()

    # Prepare the response
    the_response = make_response(clicks_data)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response