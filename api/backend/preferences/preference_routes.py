from flask import Blueprint
from backend.db_connection import get_cursor

preferences = Blueprint("preferences", __name__, url_prefix="/preferences")


@preferences.route("/", methods=["GET"])
def get_available_preferences():
    with get_cursor() as cursor:
        data = {
            "diets": {},
            "formalities": {},
            "prices": {},
            "cuisines": {},
        }

        def list_to_dict(list_data):
            return {
                item["id"]: {key: item[key] for key in item if key != "id"} for item in list_data
            }

        cursor.execute("select id, name, description from Diet_Category")
        data["diets"] = list_to_dict(cursor.fetchall())
        cursor.execute("select id, name, description from Formality")
        data["formalities"] = list_to_dict(cursor.fetchall())
        cursor.execute("select id, rating, description from Price")
        data["prices"] = list_to_dict(cursor.fetchall())
        cursor.execute("select id, name, description from Cuisine")
        data["cuisines"] = list_to_dict(cursor.fetchall())

        return data
