
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

restaurant = Blueprint('restaurant', __name__)

# Get restaurant detail for customer with particular trip id 
#restaurant inputs id for their trip and based on the city that the trip is located in, we send back restaurant recommendations sorted by least to most expensive

@restaurant.route('/restaurants/<trip_id>', methods=['GET'])
def get_restaurants_by_trip_id(trip_id):
    cursor = db.get_db().cursor()
    query = '''SELECT r.name, r.average_price, r.address, r.rating
               FROM restaurant r
               JOIN city c ON r.city_id = c.id
               JOIN trip t ON t.city_id = c.id
               WHERE t.id = %s
               ORDER BY r.average_price ASC'''
    cursor.execute(query, (trip_id,))
    restaurant_data = cursor.fetchall()

    if restaurant_data:
        return jsonify(restaurant_data), 200
    else:
        return jsonify({'error': 'No restaurants found for this trip'}), 404

@restaurant.route('/restaurant/review', methods=['POST'])
def add_new_restaurant_review():
    try:
        # Collect data from request object
        review_data = request.get_json()
        restaurant_id = review_data['restaurant_id']  # Assuming this is in the request
        trip_id = review_data['trip_id']  # Assuming this is in the request (optional)
        rating = review_data['rating']

        # Construct the query with parameter binding
        query = 'INSERT INTO restaurant_review (restaurant_id, trip_id, rating) VALUES (%s, %s, %s)'
        cursor = db.get_db().cursor()
        cursor.execute(query, (restaurant_id, trip_id, rating))
        db.get_db().commit()

        return jsonify({'message': 'Restaurant review added successfully'}), 201

    except Exception as e:
        # Handle potential errors during execution or commit
        return jsonify({'error': str(e)}), 500

