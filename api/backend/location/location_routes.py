from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

locations = Blueprint("locations", __name__)

# Helps the user choose a location based on their budgets for each respective section
# Orders the location recommendation by lowest total price
@locations.route('/budget_loc/<hotel_budget>/<flight_budget>/ \
                <attraction_budget>/<restaurant_budget>', methods = ['GET'])
def choose_loc(hotel_budget, flight_budget, attraction_budget, restaurant_budget):
    current_app.logger.info('location_routes.py: GET location based on budget')
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT country, name, SUM(flights.price + (hotel.price_per_night * trip.num_of_nights) + attraction.price + restaurant.price) AS total
        FROM city 
        JOIN trip ON city.id = trip.city_id,
        JOIN flights ON flights.city_id = city.id,
        JOIN restaurant ON restaurant.city_id = city.id,
        JOIN hotel ON hotel.city_id = city.id,
        JOIN attraction ON attraction.city_id = city.id
        WHERE flights.price <= %s,
            AND (hotel.price_per_night * trip.num_of_nights) <= %s,
            AND attraction.price <= %s,
            AND restaurant.price <= %s
        GROUP BY country, name
        HAVING total <= %s
        ORDER BY total ASC
    '''
    data = (flight_budget, hotel_budget, attraction_budget, \
        restaurant_budget, hotel_budget + flight_budget + attraction_budget + restaurant_budget)
    cursor.execute(the_query, data)

    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update the users current location
@locations.route('/current_loc', methods = ['PUT'])
def update_loc():
    current_app.logger.info('locations.route.py: PUT users location')
    # how does this connect to mockaroo data?
    loc_info = request.json
    current_city = loc_info['curr_city']
    city_id = loc_info['city_id']

    query = 'UPDATE city SET city = %s, id = %s'
    data = (current_city, city_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'address updated!'