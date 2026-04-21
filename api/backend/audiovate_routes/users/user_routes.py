
from requests import Response
from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Users routes
users = Blueprint("users", __name__)

@users.route("/<int:user_id>/artists/performance", methods=["GET"])
def get_roster_performance(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # Defaults to a wide range if dates aren't provided by the front-end
        start_date = request.args.get('start_date', '2000-01-01')
        end_date = request.args.get('end_date', '2099-12-31')

        query = """
            SELECT 
                a.artist_id,
                a.stage_name,
                s.number_of_listeners,
                s.number_of_streams,
                COALESCE(r.number_of_active_releases, 0) AS number_of_active_releases
            FROM 
                (SELECT 
                    t.track_artist_id AS artist_id,
                    COUNT(se.event_id) AS number_of_streams,
                    COUNT(DISTINCT se.event_listener_id) AS number_of_listeners
                FROM track t
                JOIN streamEvent se ON t.track_id = se.event_track_id
                WHERE se.time_stamp >= %s AND se.time_stamp <= %s
                GROUP BY t.track_artist_id) s
            JOIN artist a ON s.artist_id = a.artist_id
            JOIN manages m ON a.artist_id = m.manages_artist_id
            LEFT JOIN 
                (SELECT 
                    rel.release_artist_id AS artist_id,
                    COUNT(rel.rel_id) AS number_of_active_releases
                FROM `release` rel
                WHERE rel.release_date <= %s AND rel.status = 'Released'
                GROUP BY rel.release_artist_id) r ON a.artist_id = r.artist_id
            WHERE m.manages_user_id = %s
            ORDER BY s.number_of_streams DESC;
        """
        cursor.execute(query, (start_date, end_date, end_date, user_id))
        performance_data = cursor.fetchall()
        return jsonify(performance_data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@users.route("/", methods=["GET"])
def get_all_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()