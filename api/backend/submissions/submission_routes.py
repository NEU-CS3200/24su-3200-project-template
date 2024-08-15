from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

submissions = Blueprint('submissions', __name__)

# Get all submissions for a specific group
@submissions.route('/professors/<int:professor_id>/submissions', methods=['GET'])
def get_submissions_by_professor(professor_id):
    cursor = db.get_db().cursor()
    query = '''
    SELECT grp.group_name, sub.submission_id, sub.submitted_at, sub.submission_link,
       grp.section_num, sub.project_id
    FROM Submission sub
    JOIN `Group` grp ON sub.group_id = grp.group_id
    JOIN Section sec ON grp.section_num = sec.section_num
    WHERE sec.professor_id = %s;
    '''

    cursor.execute(query, (professor_id,))
    submissions = cursor.fetchall()
    return jsonify(submissions)