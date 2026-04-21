from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for system log routes
system_logs = Blueprint("system_logs", __name__)


# GET /system-logs - Get all system logs
@system_logs.route("/system_logs", methods=["GET"])
def get_all_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /system-logs")

        cursor.execute(
            """
            SELECT log_id, status, description, timestamp, log_user_id, log_admin_id
            FROM systemLog
            ORDER BY timestamp DESC
            """
        )
        logs = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(logs)} logs")
        return jsonify(logs), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_logs: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /system-logs - Get all error logs
@system_logs.route("/system_logs/errors", methods=["GET"])
def get_error_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /system-logs/errors")

        cursor.execute(
            """
            SELECT log_id, status, description, timestamp, log_user_id, log_admin_id
            FROM systemLog
            WHERE status = 0
            ORDER BY timestamp DESC
            """
        )
        logs = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(logs)} error logs")
        return jsonify(logs), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_error_logs: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /system-logs/<log_id> - Get a single system log by ID
@system_logs.route("/system_logs/<int:log_id>", methods=["GET"])
def get_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /system-logs/{log_id}")

        cursor.execute(
            """
            SELECT log_id, status, description, timestamp, log_user_id, log_admin_id
            FROM systemLog
            WHERE log_id = %s
            """,
            (log_id,),
        )
        log = cursor.fetchone()

        if not log:
            return jsonify({"error": "System log not found"}), 404

        return jsonify(log), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_log: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /system_logs/user/<user_id> - Get all system logs for a specific user
@system_logs.route("/system_logs/user/<int:user_id>", methods=["GET"])
def get_logs_by_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /system_logs/user/{user_id}")

        cursor.execute(
            """
            SELECT log_id, status, description, timestamp, log_user_id, log_admin_id
            FROM systemLog
            WHERE log_user_id = %s
            ORDER BY timestamp DESC
            """,
            (user_id,),
        )
        logs = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(logs)} logs for user {user_id}")
        return jsonify(logs), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_logs_by_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /system-logs/<log_id> - Update status or description of a system log [Rigby-1]
# Accepts any subset of: status, description, log_admin_id
@system_logs.route("/system_logs/<int:log_id>", methods=["PUT"])
def update_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /system-logs/{log_id}")

        data = request.get_json()

        cursor.execute(
            "SELECT log_id FROM systemLog WHERE log_id = %s", (log_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "System log not found"}), 404

        allowed_fields = ["status", "description", "log_admin_id"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(log_id)
        query = f"UPDATE systemLog SET {', '.join(update_fields)} WHERE log_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "System log updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_log: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()