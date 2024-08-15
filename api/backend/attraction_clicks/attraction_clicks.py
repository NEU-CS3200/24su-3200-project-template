from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named attraction_clicks for managing click-related routes
attraction_clicks = Blueprint('attraction_clicks', __name__)

# Route to retrieve the total clicks for a specific attraction
@attraction_clicks.route('/attraction_clicks/<attraction_id>', methods=['GET'])
def get_attraction_clicks(attraction_id):
    current_app.logger.info('attraction_clicks.py: GET /attraction_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the specified attraction_id
    the_query = '''SELECT SUM(click_counter) AS total_clicks FROM attraction_clicks WHERE attraction_id = %s'''
    cursor.execute(the_query, (attraction_id,))

    clicks_data = cursor.fetchone()

    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response