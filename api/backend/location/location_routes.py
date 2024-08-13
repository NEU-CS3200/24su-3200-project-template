from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

location = Blueprint("locations", __name__)