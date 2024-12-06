from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
)
from bcrypt import hashpw, gensalt
from backend.db_connection import db

employers = Blueprint("employers", __name__)


@employers.route("/employees", methods=["GET"])
def get_all_employees():
    query = """
        SELECT u.id, u.companyId, u.name, u.firstName, u.middleName, u.lastName, u.preferredName, u.pronouns, u.major, u.year, u.birthday, u.profilePic, u.role, u.profile, u.mobile, u.email, u.active, u.advisorId, u.companyId, u.registeredAt, u.updatedAt, u.lastLogin FROM users u 
        WHERE companyId IS NOT NULL
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/<id>/employees", methods=["GET"])
def get_employees(id):
    query = f"""
        SELECT u.*, c.name AS compName, c.id FROM users u
        JOIN companies c ON u.companyId = c.id
        WHERE c.id = {int(id)}
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/emp_company/<name>", methods=["GET"])
def get_employees_by_company(name):
    query = f"""
        SELECT u.*, c.name AS compName, c.id FROM users u
        JOIN companies c ON u.companyId = c.id
        WHERE INSTR(c.name, "{name}")
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/emp_name/<name>", methods=["GET"])
def get_employee_by_name(name):
    query = f"""
        SELECT u.*, c.name AS compName, c.id FROM users u 
        JOIN companies c ON u.companyId = c.id
        WHERE INSTR(u.name, "{name}")
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# curl http://127.0.0.1:4000/emp/1/employees -X POST -H 'Content-Type: application/json' -d '{ "firstName": "Bob", "lastName": "Marley", "email": "bmarley@google.com", "password": "P@s5w0rD", "profile": "An employee at Google" }'


@employers.route("/<id>/employees", methods=["POST"])
def add_employee(id):
    data = request.get_json()
    first_name = data["firstName"]
    last_name = data["lastName"]
    name = f"{first_name} {last_name}"
    email = data["email"]
    password = data["password"]
    profile = data["profile"]
    company_id = int(id)

    passwordHash = hashpw(password.encode("utf-8"), gensalt(12)).decode("utf-8")

    query = f"""
        INSERT INTO users (employerId, name, firstName, lastName, email, passwordHash, profile) VALUES 
        (
            "{company_id}", "{name}", "{first_name}", "{last_name}", "{email}", "{passwordHash}", "{profile}"
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/<id>/create_position", methods=["POST"])
def create_pos(id):
    data = request.get_json()
    address = data["address"]
    city = data["city"]
    country = data["country"]
    summary = data["summary"]
    applicant_questions = data["applicantQuestions"]
    expected_salary = int(data["expectedSalary"])
    company_id = int(id)

    query = f"""
        INSERT INTO positions (address, city, country, summary, applicantQuestions, expectedSalary, companyId) VALUES 
        (
            "{address}", "{city}", "{country}", "{summary}", "{applicant_questions}", {expected_salary}, {company_id}
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/<id>/positions/<pos_id>", methods=["POST"])
def offer_position(id, pos_id):
    data = request.get_json()

    query = f"""
        INSERT INTO cosint.offer_list (positionId, userId) VALUES
        (
            {int(pos_id)}, {int(data["userId"])}
        );
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@employers.route("/<id>/positions", methods=["GET"])
def get_positions(id):
    query = f"""
        SELECT p2.id, c.name AS compName, p2.registeredAt, p2.applicantQuestions, p2.summary, p2.country, p2.city, p2.address, p2.filled, p2.expectedSalary 
            FROM cosint.companies c 
            LEFT JOIN cosint.positions p2 
            ON c.id = p2.companyId
        WHERE p2.companyId = {int(id)}
        LIMIT 100;
    """

    cursor = db.get_db().cursor()

    cursor.execute(query)
    db.get_db().commit()
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
