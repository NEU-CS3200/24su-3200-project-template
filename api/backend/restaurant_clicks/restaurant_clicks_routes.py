from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named restaurant_clicks for managing click-related routes
restaurant_clicks = Blueprint('restaurant_clicks', __name__)

# Route to retrieve the total clicks for a specific restaurant
@restaurant_clicks.route('/restaurant_clicks/<restaurant_id>', methods=['GET'])
def get_restaurant_clicks(restaurant_id):
    current_app.logger.info('restaurant_clicks.py: GET /restaurant_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the specified restaurant_id
    the_query = '''SELECT SUM(click_counter) AS total_clicks FROM restaurant_clicks WHERE restaurant_id = %s'''
    cursor.execute(the_query, (restaurant_id,))

    # Fetch the data from the query result
    clicks_data = cursor.fetchone()

    # Prepare the response
    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response