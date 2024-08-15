from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named restaurant_clicks for managing click-related routes
restaurant_clicks = Blueprint('restaurant_clicks', __name__)

# Route to retrieve the total clicks for the top 5 most clicked restaurants
@restaurant_clicks.route('/restaurant_clicks', methods=['GET'])
def get_restaurant_clicks():
    current_app.logger.info('restaurant_clicks.py: GET /restaurant_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the top 5 most clicked restaurants
    the_query = '''SELECT name, SUM(click_counter) AS total_clicks 
    FROM restaurant_clicks join restaurant ON restaurant.id = restaurant_clicks.restaurant_id
    GROUP BY name
    ORDER BY total_clicks desc
    Limit 5'''
    cursor.execute(the_query)

    # Fetch the data from the query result
    clicks_data = cursor.fetchone()

    # Prepare the response
    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response