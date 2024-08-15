from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

submissions = Blueprint('submissions', __name__)

# Get all submissions for a specific group
@submissions.route('/submissions/<int:group_id>', methods=['GET'])
def get_submissions_by_group(group_id):
    cursor = db.get_db().cursor()
    query = '''
    SELECT submission_id, submitted_at, submission_link
    FROM Submission
    WHERE group_id = %s
    '''

    cursor.execute(query, (group_id,))
    submissions = cursor.fetchall()
    return jsonify(submissions)