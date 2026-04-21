from requests import Response
from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error


# Create a Blueprint for Artist routes
artists = Blueprint("artists", __name__)

@artists.route("/leaderboard", methods=["GET"])
def get_artist_leaderboard():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /artists/leaderboard")
        limit = request.args.get("limit", 10, type=int)
        query = """
            SELECT
                a.artist_id,
                a.stage_name,
                COUNT(DISTINCT r.rel_id)  AS release_count,
                COUNT(se.event_id)        AS total_streams,
                ROUND(SUM(COALESCE(se.rev_generated, 0)), 2) AS total_revenue
            FROM artist a
            LEFT JOIN track t  ON t.track_artist_id  = a.artist_id
            LEFT JOIN streamEvent se ON se.event_track_id = t.track_id
            LEFT JOIN `release` r ON r.release_artist_id = a.artist_id
            GROUP BY a.artist_id, a.stage_name
            ORDER BY total_revenue DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        for i, row in enumerate(rows, 1):
            row["rank"] = i
            row["total_revenue"] = float(row["total_revenue"])
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_artist_leaderboard: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@artists.route("/", methods=["GET"])
def get_artists():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT u.first_name, u.last_name, a.* FROM artist a
            INNER JOIN user u ON a.artist_user_id = u.user_id
        """
        cursor.execute(query)
        artists = cursor.fetchall()
        return jsonify(artists), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT
            u.first_name, 
            u.last_name, 
            a.artist_id, 
            a.stage_name, 
            a.bio, 
            a.profile_pic, 
            a.instagram
            FROM artist a
            JOIN user u ON a.artist_user_id = u.user_id
            WHERE a.artist_id = %s
        """
        cursor.execute(query, (artist_id,))
        artist = cursor.fetchone()

        if not artist:
            return jsonify({"error": "artist not found"}), 404

        # Reuse the same cursor for the follow-up queries
        cursor.execute("SELECT * FROM `release` WHERE release_artist_id = %s", (artist_id,))
        artist["releases"] = cursor.fetchall()

        return jsonify(artist), 200
    except Error as e:
        print(f"ERROR in GET artist: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/tax-status/<int:artist_id>", methods=["PUT"])
def update_tax_status(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        cursor.execute("SELECT artist_id FROM artist WHERE artist_id = %s", (artist_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Artist not found"}), 404
        # Update status
        query = "UPDATE artist SET tax_id_status = %s WHERE artist_id = %s"
        cursor.execute(query, (data["tax_id_status"], artist_id))
        get_db().commit()
        return jsonify({"message": "Tax status updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>", methods=["PUT"])
def update_artist_profile(artist_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        data = request.get_json()
        cursor.execute("SELECT artist_id FROM artist WHERE artist_id = %s", (artist_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Artist not found"}), 404
        # Build update query dynamically based on provided fields
        allowed_fields = ["bio", "instagram", "profile_pic"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(artist_id)
        query = f"UPDATE artist SET {', '.join(update_fields)} WHERE artist_id = %s"
        cursor.execute(query, params)
        db.commit()

        return jsonify({"message": "Artist profile updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/streaming-stats", methods=["GET"])
def get_monthly_stats(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
        SELECT
        t.title,
        MONTHNAME(s.time_stamp) AS month,
        COUNT(s.event_id) AS total_streams
        FROM streamEvent s
        JOIN track t ON s.event_track_id = t.track_id
        WHERE t.track_artist_id = %s
        GROUP BY t.track_id, month
        ORDER BY MAX(s.time_stamp) DESC;
"""
        cursor.execute(query, (artist_id,))
        stats = cursor.fetchall()
        return jsonify(stats), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/manages-platforms", methods=["GET"])
def get_artist_platforms(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        query = """
            SELECT 
                p.name AS platform_name,
                COUNT(se.event_id) AS total_streams,
                SUM(se.rev_generated) AS total_revenue
            FROM platform p
            JOIN streamEvent se ON p.platform_id = se.event_platform_id
            JOIN track t ON se.event_track_id = t.track_id
            JOIN artist a ON t.track_artist_id = a.artist_id
            JOIN manages m ON a.artist_id = m.manages_artist_id
            WHERE m.manages_user_id = %s AND a.artist_id = %s
            GROUP BY p.platform_id, p.name
            ORDER BY total_streams DESC;
        """
        cursor.execute(query, (user_id, artist_id))
        platforms = cursor.fetchall()
        return jsonify(platforms), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/locations", methods=["GET"])
def get_artist_locations(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        query = """
            SELECT 
                l.latitude, 
                l.longitude, 
                l.city, 
                l.country,
                COUNT(DISTINCT se.event_listener_id) AS total_listeners
            FROM location l
            JOIN streamEvent se ON l.location_id = se.event_location_id
            JOIN track t ON se.event_track_id = t.track_id
            JOIN artist a ON t.track_artist_id = a.artist_id
            JOIN manages m ON a.artist_id = m.manages_artist_id
            WHERE m.manages_user_id = %s AND a.artist_id = %s
            GROUP BY l.location_id, l.latitude, l.longitude, l.city, l.country
            ORDER BY total_listeners DESC;
        """
        cursor.execute(query, (user_id, artist_id))
        locations = cursor.fetchall()
        return jsonify(locations), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/tracks/engagement", methods=["GET"])
def get_track_engagement(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        query = """
            SELECT 
                t.title AS song_title,
                COUNT(se.event_id) AS total_streams,
                COUNT(CASE WHEN se.is_skipped = 1 THEN 1 END) AS number_of_skips
            FROM track t
            JOIN streamEvent se ON t.track_id = se.event_track_id
            JOIN artist a ON t.track_artist_id = a.artist_id
            JOIN manages m ON a.artist_id = m.manages_artist_id
            WHERE m.manages_user_id = %s AND a.artist_id = %s
            GROUP BY t.track_id, t.title
            ORDER BY number_of_skips DESC;
        """
        cursor.execute(query, (user_id, artist_id))
        engagement = cursor.fetchall()
        return jsonify(engagement), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/playlists", methods=["GET"])
def get_artist_playlists(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        query = """
            SELECT 
                pl.name AS playlist_name,
                COUNT(pe.pt_event_id) AS total_streams
            FROM playlist pl
            JOIN playlistEvent pe ON pl.playlist_id = pe.pt_playlist_id
            JOIN streamEvent se ON pe.pt_event_id = se.event_id
            JOIN track t ON se.event_track_id = t.track_id
            JOIN artist a ON t.track_artist_id = a.artist_id
            JOIN manages m ON a.artist_id = m.manages_artist_id
            WHERE m.manages_user_id = %s AND a.artist_id = %s
            GROUP BY pl.playlist_id, pl.name
            ORDER BY total_streams DESC;
        """
        cursor.execute(query, (user_id, artist_id))
        playlists = cursor.fetchall()
        return jsonify(playlists), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@artists.route("/<int:artist_id>/tracks", methods=["GET"])
def get_artist_tracks(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /artists/{artist_id}/tracks")
        
        # Joining the release table to grab the release title alongside the track info
        query = """
            SELECT 
                t.track_id, 
                t.title, 
                t.genre, 
                t.isrc_code,
                r.rel_id AS release_id,
                r.title AS release_title,
                r.release_date
            FROM track t
            JOIN `release` r ON t.track_release_id = r.rel_id
            WHERE t.track_artist_id = %s
            ORDER BY r.release_date DESC, t.track_id ASC;
        """
        cursor.execute(query, (artist_id,))
        tracks = cursor.fetchall()
        
        return jsonify(tracks), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_artist_tracks: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


#For artist
@artists.route("/<int:artist_id>/platforms", methods=["GET"])
def get_artist_platforms_single(artist_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        
        query = """
            SELECT 
                p.name AS platform_name,
                COUNT(se.event_id) AS total_streams,
                SUM(se.rev_generated) AS total_revenue
            FROM platform p
            JOIN streamEvent se ON p.platform_id = se.event_platform_id
            JOIN track t ON se.event_track_id = t.track_id
            -- Join directly to artist, no 'manages' table needed
            WHERE t.track_artist_id = %s 
            GROUP BY p.platform_id, p.name
            ORDER BY total_streams DESC;
        """
        cursor.execute(query, (artist_id,))
        platforms = cursor.fetchall()
        return jsonify(platforms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()