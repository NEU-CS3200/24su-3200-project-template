from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

submissions = Blueprint('submissions', __name__)

# Get all submissions for a specific group
@submissions.route('/submissions/<email>', methods=['GET'])
def get_prof_subs(email):
    cursor = db.get_db().cursor()

    # Use parameterized query to prevent SQL injection
    query_id = '''SELECT professor_id
                FROM Professor
                WHERE email=%s;'''
    cursor.execute(query_id, (email))
    theData = cursor.fetchone()

    if theData:
        prof_id = theData["professor_id"]
        
        query = '''SELECT grp.group_name, sub.submission_id, sub.submitted_at, sub.submission_link,
         grp.section_num, sub.project_id
         FROM Submission sub
         JOIN `Group` grp ON sub.group_id = grp.group_id
         JOIN Section sec ON grp.section_num = sec.section_num
      WHERE sec.professor_id = %s;'''
        cursor.execute(query, (prof_id))
        sub_data = cursor.fetchall()
        the_response = make_response(jsonify(sub_data))
    else:
        # Return an error if the TA is not found
        the_response = make_response(jsonify({'error': 'No available submissions'}), 404)
    
    the_response.mimetype = 'application/json'
    return the_response