from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
from backend.db_connection import db

# This blueprint handles some basic routes that you can use for testing
simple_routes = Blueprint("simple_routes", __name__)


# ------------------------------------------------------------
# / is the most basic route
# Once the api container is started, in a browser, go to
# localhost:4000/playlist
@simple_routes.route("/")
def welcome():
    current_app.logger.info("GET / handler")
    welcome_message = "<h1>Welcome to the cosint REST API</h1>"
    response = make_response(welcome_message)
    response.status_code = 200
    return response


@simple_routes.route("/test")
def api_test():
    message = "API is working"
    response = make_response(jsonify({"message": message}))
    response.status_code = 200
    return response


@simple_routes.route("/create_help_ticket", methods=["POST"])
def create_help_ticket():
    data = request.get_json()
    user_id = str(data["userId"])
    summary = str(data["summary"])

    query = f"""
        INSERT INTO tickets (userId, summary, completed) VALUES
        (
            {user_id}, "{summary}", 0
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@simple_routes.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    query = f"""
        SELECT u.id, u.studentId, u.name, u.firstName, u.middleName, u.lastName, u.preferredName, u.pronouns, u.major, u.year, u.birthday, u.profilePic, u.role, u.profile, u.mobile, u.email, u.active, u.advisorId, u.companyId, u.registeredAt, u.updatedAt, u.lastLogin 
        FROM users u 
        WHERE u.id = {int(user_id)}
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@simple_routes.route("/users/<id>", methods=["PUT"])
def update_users(id):
    data = request.get_json()

    query = f"""
        SELECT * FROM users
        WHERE id = {int(id)};
    """
    cursor = db.get_db().cursor()

    cursor.execute(query)
    student = cursor.fetchall()[0]

    if len(student) == 0:
        response = make_response(jsonify({"message": "id not found"}))
        response.status_code = 404
        return response

    query = "UPDATE users "

    if len(data) > 1:
        query += "SET "

    for key in data:
        if key in student and key != "id":
            if type(data[key]) is int:
                query = query + f"{key} = {data[key]}, "
            else:
                query = query + f'{key} = "{data[key]}", '

    query = query[:-2] + f" WHERE id = {int(id)};"

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
