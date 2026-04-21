from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for payout profile routes (Marcus - Label Head, Jessica - Artist)
payout_profiles = Blueprint("payout_profiles", __name__)


def _serialize(profile):
    """Cast Decimal fields to float so jsonify always returns a number."""
    if profile and "split_percentage" in profile:
        profile["split_percentage"] = float(profile["split_percentage"])
    return profile


# GET /payoutProfiles - Get all payout profiles; filter by release_id query param [Marcus-2]
# Example: /payoutProfiles?release_id=3
@payout_profiles.route("/", methods=["GET"])
def get_all_payout_profiles():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /payoutProfiles")

        release_id = request.args.get("release_id")

        query = """
            SELECT pp.*, r.title AS release_title, a.stage_name AS artist_name
            FROM payoutProfiles pp
            JOIN `release` r ON pp.pp_release_id = r.rel_id
            JOIN artist a ON r.release_artist_id = a.artist_id
            WHERE 1=1
        """
        params = []

        if release_id:
            query += " AND pp.pp_release_id = %s"
            params.append(release_id)

        cursor.execute(query, params)
        profiles = [_serialize(p) for p in cursor.fetchall()]

        current_app.logger.info(f"Retrieved {len(profiles)} payout profiles")
        return jsonify(profiles), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_payout_profiles: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /payoutProfiles/<payout_id> - Get a single payout profile by ID
@payout_profiles.route("/<int:payout_id>", methods=["GET"])
def get_payout_profile(payout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /payoutProfiles/{payout_id}")

        cursor.execute(
            """
            SELECT pp.*, r.title AS release_title, a.stage_name AS artist_name
            FROM payoutProfiles pp
            JOIN `release` r ON pp.pp_release_id = r.rel_id
            JOIN artist a ON r.release_artist_id = a.artist_id
            WHERE pp.payout_id = %s
            """,
            (payout_id,),
        )
        profile = cursor.fetchone()

        if not profile:
            return jsonify({"error": "Payout profile not found"}), 404

        return jsonify(_serialize(profile)), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_payout_profile: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /payoutProfiles/release/<release_id> - Get all payout profiles for a release [Marcus-2, Jessica-6]
@payout_profiles.route("/release/<int:release_id>", methods=["GET"])
def get_payout_profiles_by_release(release_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /payoutProfiles/release/{release_id}")

        cursor.execute(
            "SELECT rel_id FROM `release` WHERE rel_id = %s", (release_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Release not found"}), 404

        cursor.execute(
            """
            SELECT pp.*, r.title AS release_title, a.stage_name AS artist_name
            FROM payoutProfiles pp
            JOIN `release` r ON pp.pp_release_id = r.rel_id
            JOIN artist a ON r.release_artist_id = a.artist_id
            WHERE pp.pp_release_id = %s
            """,
            (release_id,),
        )
        profiles = [_serialize(p) for p in cursor.fetchall()]

        return jsonify(profiles), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_payout_profiles_by_release: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /payoutProfiles - Add a new collaborator payout profile [Marcus-1, Jessica-6]
# Required JSON body: collab_email, role, split_percentage, pp_release_id
@payout_profiles.route("/", methods=["POST"])
def create_payout_profile():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /payoutProfiles")

        data = request.get_json()

        required_fields = ["collab_email", "role", "split_percentage", "pp_release_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Verify the release exists before inserting
        cursor.execute(
            "SELECT rel_id FROM `release` WHERE rel_id = %s", (data["pp_release_id"],)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Release not found"}), 404

        query = """
            INSERT INTO payoutProfiles (collab_email, role, split_percentage, pp_release_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["collab_email"],
            data["role"],
            data["split_percentage"],
            data["pp_release_id"],
        ))
        get_db().commit()

        return jsonify({
            "message": "Payout profile created successfully",
            "payout_id": cursor.lastrowid,
        }), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_payout_profile: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /payoutProfiles/<payout_id> - Update royalty split percentage (or role/email) [Marcus-2]
# Accepts any subset of: collab_email, role, split_percentage
@payout_profiles.route("/<int:payout_id>", methods=["PUT"])
def update_payout_profile(payout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /payoutProfiles/{payout_id}")

        data = request.get_json()

        cursor.execute(
            "SELECT payout_id FROM payoutProfiles WHERE payout_id = %s", (payout_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Payout profile not found"}), 404

        allowed_fields = ["collab_email", "role", "split_percentage"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(payout_id)
        query = f"UPDATE payoutProfiles SET {', '.join(update_fields)} WHERE payout_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Payout profile updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_payout_profile: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /payoutProfiles/<payout_id> - Remove a collaborator payout profile from a release
@payout_profiles.route("/<int:payout_id>", methods=["DELETE"])
def delete_payout_profile(payout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /payoutProfiles/{payout_id}")

        cursor.execute(
            "SELECT payout_id FROM payoutProfiles WHERE payout_id = %s", (payout_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Payout profile not found"}), 404

        cursor.execute(
            "DELETE FROM payoutProfiles WHERE payout_id = %s", (payout_id,)
        )
        get_db().commit()

        return jsonify({"message": "Payout profile deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_payout_profile: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
