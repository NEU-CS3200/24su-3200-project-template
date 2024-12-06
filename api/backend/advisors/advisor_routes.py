from flask import (
    Blueprint,
    jsonify,
    make_response,
)
from backend.db_connection import db

advisors = Blueprint("advisors", __name__)

# curl http://127.0.0.1:4000/adv/advisors -X GET


@advisors.route("/advisors", methods=["GET"])
def get_advisors():
    query = """
        SELECT * FROM users u
        WHERE u.companyId IS NULL AND u.advisorId IS NULL AND u.studentId IS NULL
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/adv/advisors/1 -X GET


@advisors.route("/advisors/<id>", methods=["GET"])
def get_advisor_by_id(id):
    query = f"""
        SELECT * FROM users u
        WHERE u.companyId IS NULL AND u.advisorId IS NULL AND u.studentId IS NULL AND u.id = {int(id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/adv/advisors/1/students -X GET


@advisors.route("/advisors/<id>/students", methods=["GET"])
def get_advisor_students(id):
    query = f"""
        SELECT * FROM users u
        WHERE u.advisorId = {int(id)} AND u.studentId IS NOT NULL
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@advisors.route("/advisors/<id>/students/count", methods=["GET"])
def get_advisor_students_count(id):
    query = f"""
        SELECT COUNT(*) FROM cosint.users u
        WHERE u.advisorId = {int(id)} AND u.companyId IS NOT NULL;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
