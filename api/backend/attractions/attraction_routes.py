from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

attractions = Blueprint("attractions", __name__)

@attractions.route()
def get_attractions():
    the_query = '''
        Select attraction_name
        From attractions
    '''
    cursor.execute(the_query)
