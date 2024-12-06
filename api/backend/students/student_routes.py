from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
from bcrypt import hashpw, gensalt
from backend.db_connection import db

students = Blueprint("students", __name__)


# Example of a POST request
# curl http://127.0.0.1:4000/stu/create -X POST -H 'Content-Type: application/json' -d '{ "studentId": "010101010", "firstName": "Sam", "lastName": "Ehlers", "email": "ehlers.s@northeastern.edu", "password": "P@s5w0rD", "profile": "A student at northeastern university" }'


@students.route("/create", methods=["POST"])
def create_student():
    data = request.get_json()
    student_id = data["studentId"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    name = f"{first_name} {last_name}"
    email = data["email"]
    password = data["password"]
    profile = data["profile"]

    passwordHash = hashpw(password.encode("utf-8"), gensalt(12)).decode("utf-8")

    query = f"""
        INSERT INTO users (studentId, name, firstName, lastName, email, passwordHash, profile) VALUES 
        (
            "{student_id}", "{name}", "{first_name}", "{last_name}", "{email}", "{passwordHash}", "{profile}"
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@students.route("/bookmark_company", methods=["POST"])
def add_bookmark():
    data = request.get_json()
    stu_id = int(data["studentId"])
    pos_id = int(data["positionId"])

    query = f"""
        INSERT INTO position_user_bookmark (positionId, userId) VALUES
        (
            {pos_id}, {stu_id}
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@students.route("/user_reference", methods=["POST"])
def add_user_reference():
    data = request.get_json()
    user_id = int(data["studentId"])
    name = data["name"]
    firstName = data["firstName"]
    middleName = data["middleName"]
    lastName = data["lastName"]
    mobile = data["mobile"]
    email = data["email"]
    referral = data["referral"]

    query = f"""
        INSERT INTO user_references (userId, name, firstName, middleName, lastName, mobile, email, referral) VALUES
        (
            {user_id}, "{name}", "{firstName}", "{middleName}", "{lastName}", "{mobile}", "{email}", "{referral}"
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/stu/students -X GET


@students.route("/students", methods=["GET"])
def get_students():
    query = """
        SELECT u.id, u.studentId, u.name, u.firstName, u.middleName, u.lastName, u.preferredName, u.pronouns, u.major, u.year, u.birthday, u.profilePic, u.role, u.profile, u.mobile, u.email, u.active, u.advisorId, u.companyId, u.registeredAt, u.updatedAt, u.lastLogin FROM users u 
        WHERE studentId IS NOT NULL
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/stu/students/010101010 -X GET


@students.route("/students/<student_id>", methods=["GET"])
def get_student_by_id(student_id):
    query = f"""
        SELECT u.id, u.studentId, u.name, u.firstName, u.middleName, u.lastName, u.preferredName, u.pronouns, u.major, u.year, u.birthday, u.profilePic, u.role, u.profile, u.mobile, u.email, u.active, u.advisorId, u.companyId, u.registeredAt, u.updatedAt, u.lastLogin FROM users u 
        WHERE studentId = {int(student_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/stu/students/010101010/applications -X GET


@students.route("/students/<student_id>/applications", methods=["GET"])
def get_student_applications(student_id):
    query = f"""
        SELECT a.* FROM applications a 
            JOIN application_bookmark o ON a.id = o.applicationId
            JOIN users u ON o.userId = u.id
        WHERE u.studentId = {int(student_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/stu/students/010101010/advisor -X GET


@students.route("/students/<student_id>/advisor", methods=["GET"])
def get_student_advisor(student_id):
    query = f"""
        SELECT a.* FROM users u 
            JOIN users a ON u.advisorId = a.id 
        WHERE u.studentId = {int(student_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@students.route("/students/<student_id>/progress", methods=["GET"])
def get_progress(student_id):
    query = f"""
        SELECT (COUNT(*)/3) * 100 AS progress FROM cosint.users u
            JOIN cosint.application_bookmark ab on u.id = ab.userId
            JOIN cosint.applications a on ab.applicationId = a.id
            JOIN cosint.related_coursework r ON a.id = r.applicationId
            JOIN cosint.notable_skills n ON a.id = n.applicationId
            JOIN cosint.work_experience we ON a.id = we.applicationId
        WHERE u.studentId = {int(student_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/stu/students/search/sam -X GET


@students.route("/students/search/<res>", methods=["GET"])
def student_search(res):
    query = f"""
        SELECT u.id, u.studentId, u.name, u.firstName, u.middleName, u.lastName, u.preferredName, u.pronouns, u.major, u.year, u.birthday, u.profilePic, u.role, u.profile, u.mobile, u.email, u.active, u.advisorId, u.companyId, u.registeredAt, u.updatedAt, u.lastLogin FROM users u
        WHERE INSTR(u.name, "{res}") OR INSTR(u.email, "{res}")
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Example of a PUT request
# curl http://127.0.0.1:4000/stu/students/010101010/update -X PUT -H 'Content-Type: application/json' -d '{ "studentId": "010101010", "firstName": "Bob", "mobile": "1234567899" }'


@students.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    if student_id != data["studentId"]:
        response = make_response(
            jsonify({"message": "student_id in URL does not match student_id in body"})
        )
        response.status_code = 400
        return response

    query = f"""
        SELECT * FROM users
        WHERE studentId = {int(student_id)};
    """
    cursor = db.get_db().cursor()

    cursor.execute(query)
    student = cursor.fetchall()[0]

    if len(student) == 0:
        response = make_response(jsonify({"message": "student_id not found"}))
        response.status_code = 404
        return response

    query = "UPDATE users "

    if len(data) > 1:
        query += "SET "

    for key in data:
        if key in student and key != "studentId":
            if type(data[key]) is int:
                query = query + f"{key} = {data[key]}, "
            else:
                query = query + f'{key} = "{data[key]}", '

    query = query[:-2] + f" WHERE studentId = {int(student_id)};"

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Example of a DELETE request
# curl http://127.0.0.1:4000/stu/students/010101010/delete -X DELETE


@students.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    query = f"""
        DELETE FROM users
        WHERE studentId = {int(student_id)};
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
