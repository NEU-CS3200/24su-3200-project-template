from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for help request routes (Rigby - System Admin)
help_requests = Blueprint("help_requests", __name__)


# GET /help-requests - Get all help requests
@help_requests.route("/help_requests", methods=["GET"])
def get_all_requests():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /help-requests")

        cursor.execute(
            """
            SELECT request_id, created_at, submitted_user_id, status, description, assigned_admin_id
            FROM helpRequest
            ORDER BY created_at DESC
            """
        )
        requests_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(requests_list)} help requests")
        return jsonify(requests_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_requests: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /help-requests - Get all unresolved help requests
@help_requests.route("/help_requests/status", methods=["GET"])
def get_open_requests():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /help-requests/open")

        cursor.execute(
            """
            SELECT request_id, created_at, description, status, submitted_user_id, assigned_admin_id
            FROM helpRequest
            WHERE status = 0
            ORDER BY created_at DESC
            """
        )
        requests_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(requests_list)} open help requests")
        return jsonify(requests_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_open_requests: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /help-requests/<request_id> - Get a single help request by ID
@help_requests.route("/help_requests/<int:request_id>", methods=["GET"])
def get_request(request_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /help-requests/{request_id}")

        cursor.execute(
            """
            SELECT request_id, created_at, submitted_user_id, status, description, assigned_admin_id
            FROM helpRequest
            WHERE request_id = %s
            """,
            (request_id,),
        )
        req = cursor.fetchone()

        if not req:
            return jsonify({"error": "Help request not found"}), 404

        return jsonify(req), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_request: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /help_requests/by-admin - Get help request counts by admin [Rigby-4]
@help_requests.route("/help_requests/by-admin", methods=["GET"])
def get_requests_by_admin():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /help-requests/by-admin")

        cursor.execute(
            """
            SELECT assigned_admin_id, COUNT(*) AS request_count
            FROM helpRequest
            GROUP BY assigned_admin_id
            ORDER BY request_count DESC
            """
        )
        data = cursor.fetchall()

        current_app.logger.info(f"Retrieved workload data for {len(data)} admins")
        return jsonify(data), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_requests_by_admin: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /help_requests/by-user - Get help request counts by user [Rigby-6]
@help_requests.route("/help_requests/by-user", methods=["GET"])
def get_requests_by_user():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /help-requests/by-user")

        cursor.execute(
            """
            SELECT submitted_user_id, COUNT(*) AS help_request_count
            FROM helpRequest
            GROUP BY submitted_user_id
            ORDER BY help_request_count DESC
            """
        )
        data = cursor.fetchall()

        current_app.logger.info(f"Retrieved help request counts for {len(data)} users")
        return jsonify(data), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_requests_by_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /help-requests - Create a new help request
@help_requests.route("/help_requests", methods=["POST"])
def create_request():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /help-requests")

        data = request.get_json()

        required_fields = ["submitted_user_id", "description", "assigned_admin_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        status = data.get("status", 0)

        query = """
            INSERT INTO helpRequest (submitted_user_id, status, description, assigned_admin_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["submitted_user_id"],
            status,
            data["description"],
            data["assigned_admin_id"],
        ))
        get_db().commit()

        return jsonify({
            "message": "Help request created successfully",
            "request_id": cursor.lastrowid,
        }), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_request: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /help-requests/<request_id> - Update status or assigned admin of a help request
# Accepts any subset of: status, description, assigned_admin_id
@help_requests.route("/help_requests/<int:request_id>", methods=["PUT"])
def update_request(request_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /help-requests/{request_id}")

        data = request.get_json()

        cursor.execute(
            "SELECT request_id FROM helpRequest WHERE request_id = %s", (request_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Help request not found"}), 404

        allowed_fields = ["status", "description", "assigned_admin_id"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(request_id)
        query = f"UPDATE helpRequest SET {', '.join(update_fields)} WHERE request_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Help request updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_request: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()