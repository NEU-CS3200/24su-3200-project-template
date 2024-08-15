from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint named attraction_clicks for managing click-related routes
attraction_clicks = Blueprint('attraction_clicks', __name__)

# Route to retrieve the total clicks for the most clicked attractions
@attraction_clicks.route('/attraction_clicks', methods=['GET'])
def get_attraction_clicks():
    current_app.logger.info(f'attraction_clicks.py: GET /attraction_clicks')
    cursor = db.get_db().cursor()

    # Execute a SQL query to fetch the sum of clicks for the top 5 attractions with the most clicks
    the_query = '''SELECT name, SUM(click_counter) AS total_clicks 
    FROM attraction_clicks join attraction ON attraction.id = attraction_clicks.attraction_id
    GROUP BY name
    ORDER BY total_clicks desc
    Limit 5'''
    cursor.execute(the_query)

    clicks_data = cursor.fetchall()

    the_response = make_response(jsonify(clicks_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response