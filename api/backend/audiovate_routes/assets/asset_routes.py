from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for asset routes (Marcus - Label Head, Jessica - Artist)
assets = Blueprint("assets", __name__)


# GET /assets - Get all assets; optional filters: upload_status, file_type [Marcus-6]
# Example: /assets?upload_status=0&file_type=Audio
@assets.route("/", methods=["GET"])
def get_all_assets():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /assets")

        upload_status = request.args.get("upload_status")
        file_type = request.args.get("file_type")

        query = """
            SELECT a.*, r.title AS release_title, ar.stage_name AS artist_name
            FROM asset a
            JOIN `release` r ON a.asset_release_id = r.rel_id
            JOIN artist ar ON r.release_artist_id = ar.artist_id
            WHERE 1=1
        """
        params = []

        if upload_status is not None:
            query += " AND a.upload_status = %s"
            params.append(upload_status)

        if file_type:
            query += " AND a.file_type = %s"
            params.append(file_type)

        cursor.execute(query, params)
        asset_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(asset_list)} assets")
        return jsonify(asset_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_assets: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /assets/<asset_id> - Get a single asset by ID
@assets.route("/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /assets/{asset_id}")

        cursor.execute(
            """
            SELECT a.*, r.title AS release_title, ar.stage_name AS artist_name
            FROM asset a
            JOIN `release` r ON a.asset_release_id = r.rel_id
            JOIN artist ar ON r.release_artist_id = ar.artist_id
            WHERE a.asset_id = %s
            """,
            (asset_id,),
        )
        asset = cursor.fetchone()

        if not asset:
            return jsonify({"error": "Asset not found"}), 404

        return jsonify(asset), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_asset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /assets/release/<release_id> - Get all assets for a specific release [Marcus-6, Jessica-1]
@assets.route("/release/<int:release_id>", methods=["GET"])
def get_assets_by_release(release_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /assets/release/{release_id}")

        cursor.execute(
            "SELECT rel_id FROM `release` WHERE rel_id = %s", (release_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Release not found"}), 404

        cursor.execute(
            """
            SELECT a.*, r.title AS release_title, ar.stage_name AS artist_name
            FROM asset a
            JOIN `release` r ON a.asset_release_id = r.rel_id
            JOIN artist ar ON r.release_artist_id = ar.artist_id
            WHERE a.asset_release_id = %s
            ORDER BY a.file_type
            """,
            (release_id,),
        )
        asset_list = cursor.fetchall()

        return jsonify(asset_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_assets_by_release: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /assets/release/<release_id> - Upload a new asset for a release [Jessica-1, Marcus-6]
# Required JSON body: file_url, file_type ("Audio" | "Artwork" | "Credits")
# Optional: upload_status (defaults to 0 = pending)
@assets.route("/release/<int:release_id>", methods=["POST"])
def create_asset(release_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /assets/release/{release_id}")

        data = request.get_json()

        required_fields = ["file_url", "file_type"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        valid_file_types = ["Audio", "Artwork", "Credits"]
        if data["file_type"] not in valid_file_types:
            return jsonify({"error": f"file_type must be one of {valid_file_types}"}), 400

        # Verify the release exists before inserting
        cursor.execute(
            "SELECT rel_id FROM `release` WHERE rel_id = %s", (release_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Release not found"}), 404

        upload_status = data.get("upload_status", 0)

        query = """
            INSERT INTO asset (file_url, file_type, upload_status, asset_release_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["file_url"],
            data["file_type"],
            upload_status,
            release_id,
        ))
        get_db().commit()

        return jsonify({
            "message": "Asset created successfully",
            "asset_id": cursor.lastrowid,
        }), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_asset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /assets/<asset_id> - Update file URL or upload status before release [Jessica-3]
# Accepts any subset of: file_url, file_type, upload_status
@assets.route("/<int:asset_id>", methods=["PUT"])
def update_asset(asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /assets/{asset_id}")

        data = request.get_json()

        cursor.execute(
            "SELECT asset_id FROM asset WHERE asset_id = %s", (asset_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Asset not found"}), 404

        allowed_fields = ["file_url", "file_type", "upload_status"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(asset_id)
        query = f"UPDATE asset SET {', '.join(update_fields)} WHERE asset_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Asset updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_asset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /assets/<asset_id> - Remove an asset from a release
@assets.route("/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /assets/{asset_id}")

        cursor.execute(
            "SELECT asset_id FROM asset WHERE asset_id = %s", (asset_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Asset not found"}), 404

        cursor.execute("DELETE FROM asset WHERE asset_id = %s", (asset_id,))
        get_db().commit()

        return jsonify({"message": "Asset deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_asset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
