from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

companyProfiles = Blueprint('companyProfiles', __name__)

# Student/Advisor views a company profile
@companyProfiles.route('/companyProfiles/<companyProfileId>', methods=['GET'])
def get_company_profile(companyProfileId):
    query = '''
        SELECT companyProfileId, name, bio, industry, websiteLink
        FROM companyProfiles
        WHERE companyProfileId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (companyProfileId,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Advisor views all company profiles
@companyProfiles.route('/companyProfiles', methods=['GET'])
def get_all_company_profiles():
    query = '''
        SELECT companyProfileId, name, bio, industry, websiteLink
        FROM companyProfiles
        ORDER BY name
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response