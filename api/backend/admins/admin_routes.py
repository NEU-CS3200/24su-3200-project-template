from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

admins = Blueprint("admins", __name__)


@admins.route("/<com_id>/coop_rep", methods=["GET"])
def get_reps(com_id):
    data = request.get_json()
    query = f"""
        SELECT u.firstName, u.middleName, u.lastName, u.mobile, u.email FROM cosint.users u
        WHERE u.firstName = '{data["firstName"]}' AND u.lastName = '{data["lastName"]}' AND u.companyId = {int(com_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/add_company", methods=["POST"])
def add_company():
    data = request.get_json()
    comp_name = data["name"]

    query = f"""
        INSERT INTO cosint.companies (name) VALUES
        (
            {comp_name}
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/rawsql", methods=["GET"])
def rawsql():
    data = request.get_json()
    query = data["query"]

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/tickets", methods=["GET"])
def get_tickets():
    query = """
        SELECT u.name AS 'helping', h.name AS 'assignedTo', t.summary, t.completed, t.updatedAt, t.registeredAt FROM cosint.tickets t
        LEFT JOIN cosint.users u ON t.helperId = u.id
        JOIN cosint.users h ON t.userId = h.id
        WHERE completed = 0;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/tickets/<ticket_id>", methods=["GET"])
def get_tickets_by_id(ticket_id):
    query = f"""
        SELECT u.name AS 'helping', h.name AS 'assignedTo', t.summary, t.completed, t.updatedAt, t.registeredAt FROM cosint.tickets t
        LEFT JOIN cosint.users u ON t.helperId = u.id
        JOIN cosint.users h ON t.userId = h.id
        WHERE completed = 0 and t.id = {int(ticket_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/tickets/<id>", methods=["PUT"])
def update_ticket(id):
    data = request.get_json()
    if int(id) != int(data["id"]):
        response = make_response(
            jsonify({"message": "id in URL does not match id in body"})
        )
        response.status_code = 400
        return response

    query = f"""
        SELECT * FROM tickets
        WHERE id = {int(id)};
    """
    cursor = db.get_db().cursor()

    cursor.execute(query)
    student = cursor.fetchall()[0]

    if len(student) == 0:
        response = make_response(jsonify({"message": "id not found"}))
        response.status_code = 404
        return response

    query = "UPDATE tickets "

    if len(data) > 1:
        query += "SET "

    for key in data:
        if key in student and key != "studentId":
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


@admins.route("/stats", methods=["GET"])
def stats():
    query = """
        SELECT
            MIN(lastLogin) AS intervalStart,
            DATE_ADD(MIN(lastLogin), INTERVAL 15 MINUTE) AS intervalEnd,
            COUNT(*) AS loginCount
        FROM cosint.users u
        WHERE lastLogin BETWEEN u.lastLogin AND DATE_ADD(u.lastLogin, INTERVAL 15 MINUTE)
        GROUP BY u.lastLogin
        ORDER BY loginCount DESC
        LIMIT 5;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@admins.route("/delete_user", methods=["DELETE"])
def remove_user(user_id):
    query = f"""
        DELETE FROM cosint.users u WHERE u.id = {int(user_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
