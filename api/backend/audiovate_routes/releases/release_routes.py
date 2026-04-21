from requests import Response
from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error


# Create a Blueprint for Release routes
releases = Blueprint("releases", __name__)

@releases.route("/releases/<int:artist_id>", methods=["POST"])
def create_release(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        release_query = """
            INSERT INTO `release` (release_artist_id, title, type, release_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        release_values = (artist_id, data["title"], data["type"], data["release_date"], 'Processing')
        cursor.execute(release_query, release_values)
        
        new_release_id = cursor.lastrowid

        track_query = """
            INSERT INTO track (title, genre, isrc_code, track_artist_id, track_release_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        for track in data.get("tracks", []):
            track_values = (track["title"], track["genre"], track["isrc_code"], artist_id, new_release_id)
            cursor.execute(track_query, track_values)
        
        assert_query = """
            INSERT INTO asset (file_url, file_type, upload_status, asset_release_id)
            VALUES (%s, %s, %s, %s)
        """
        for asset in data.get("assets", []):
            asset_values = (asset["file_url"], asset["file_type"], 'Processing', new_release_id)
            cursor.execute(assert_query, asset_values)

        get_db().commit()

        return jsonify({"message": "Release created successfully", "release_id": new_release_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/releases", methods=["GET"])
def get_all_releases():
    cursor = get_db().cursor(dictionary=True)
    status_filter = request.args.get('status')

    try:
        if status_filter:
            cursor.execute("SELECT * FROM `release` WHERE status = %s", (status_filter,))
        else:
            cursor.execute("SELECT * FROM `release`")

        releases = cursor.fetchall()
        return jsonify(releases), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/releases/roster-status", methods=["GET"])
def get_roster_status():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT r.rel_id, r.title, r.status, r.release_date, a.stage_name
            FROM `release` r
            JOIN artist a ON r.release_artist_id = a.artist_id
            ORDER BY r.release_date ASC
        """
        cursor.execute(query)
        releases = cursor.fetchall()
        return jsonify(releases), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/releases/rankings", methods=["GET"])
def get_release_rankings():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT a.stage_name, COUNT(r.rel_id) as release_count
            FROM artist a
            LEFT JOIN `release` r ON a.artist_id = r.release_artist_id
            GROUP BY a.artist_id
            ORDER BY release_count DESC
        """
        cursor.execute(query)
        releases = cursor.fetchall()
        return jsonify(releases), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/releases/<int:release_id>", methods=["DELETE"])
def delete_release(release_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT track_id FROM track WHERE track_release_id = %s", (release_id,))
        tracks = cursor.fetchall()
        track_ids = [t[0] if isinstance(t, tuple) else t['track_id'] for t in tracks]

        if track_ids:
        # 2. Delete Stream Events for these tracks
            format_strings = ','.join(['%s'] * len(track_ids))
            cursor.execute(f"DELETE FROM streamEvent WHERE event_track_id IN ({format_strings})", tuple(track_ids))

            # 3. Delete Tracks
            cursor.execute("DELETE FROM track WHERE track_release_id = %s", (release_id,))

            # 4. Delete Payout Profiles
            cursor.execute("DELETE FROM payoutProfiles WHERE pp_release_id = %s", (release_id,))
        
            # 5. Delete Assets
            cursor.execute("DELETE FROM asset WHERE asset_release_id = %s", (release_id,))

            # 6. delete the Release
            cursor.execute("DELETE FROM `release` WHERE rel_id = %s", (release_id,))
            db.commit()
            return jsonify({"message": "Release deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/release/<int:release_id>", methods=["PUT"])
def update_release(release_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        allowed_fields = ["status", "release_date", "title", "type"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(release_id)
        query = f"UPDATE `release` SET {', '.join(update_fields)} WHERE rel_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Release updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/streams/top-earners", methods=["GET"])
def get_top_earners():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT
                a.stage_name,
                SUM(s.rev_generated) AS total_revenue,
                COUNT(s.event_id) AS total_streams
            FROM streamEvent s
            JOIN track t ON s.event_track_id = t.track_id
            JOIN artist a ON t.track_artist_id = a.artist_id
            GROUP BY a.artist_id
            ORDER BY total_revenue DESC
            LIMIT 10
        """
        cursor.execute(query)
        top_earners = cursor.fetchall()
        return jsonify(top_earners), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@releases.route("/releases/<int:release_id>/tracks", methods=["GET", "POST"])
def manage_release_tracks(release_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # First, verify the release exists and get its artist_id
        cursor.execute("SELECT release_artist_id FROM `release` WHERE rel_id = %s", (release_id,))
        release = cursor.fetchone()
        
        if not release:
            return jsonify({"error": "Release not found"}), 404

        # Handle GET: Return all tracks for this release
        if request.method == "GET":
            current_app.logger.info(f"GET /releases/{release_id}/tracks")
            cursor.execute("SELECT * FROM track WHERE track_release_id = %s", (release_id,))
            tracks = cursor.fetchall()
            return jsonify(tracks), 200

        # Handle POST: Create a new track for this release
        elif request.method == "POST":
            current_app.logger.info(f"POST /releases/{release_id}/tracks")
            data = request.get_json()
            
            required_fields = ["title", "genre", "isrc_code"]
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            query = """
                INSERT INTO track (title, genre, isrc_code, track_artist_id, track_release_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["title"],
                data["genre"],
                data["isrc_code"],
                release["release_artist_id"], # Inherited securely from the release
                release_id
            ))
            get_db().commit()
            
            return jsonify({
                "message": "Track created successfully", 
                "track_id": cursor.lastrowid
            }), 201

    except Error as e:
        current_app.logger.error(f"Database error in manage_release_tracks: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
