from flask import Blueprint
from backend.db_connection import get_cursor

customers = Blueprint("customers", __name__, url_prefix="/customers")


# Get customer detail for customer with particular <cust_id>
# Includes basic info like name and email as well as preference data
@customers.route("/<cust_id>", methods=["GET"])
def get_customer(cust_id):
    with get_cursor() as cursor:
        cursor.execute(
            """
        select firstName, middleInitial, lastName, email, longitude, latitude
        from Customer
        where id = %s
        """,
            cust_id,
        )
        data = cursor.fetchall()
        if data:
            cust_data = data[0]

            # Helper method for joining Customer with a preference-related table
            def get_cust_pref(pref_table_name, cust_id, short_name=None):
                if not short_name:
                    short_name = pref_table_name

                with get_cursor() as inner_cursor:
                    inner_cursor.execute(
                        f"""
                    select id
                    from Cust_{short_name} a
                    join {pref_table_name} b on a.{short_name}Id = b.id
                    where a.custId = %s
                    """,
                        cust_id,
                    )
                    ids = inner_cursor.fetchall()
                    return [item["id"] for item in ids]

            cust_data["prices"] = get_cust_pref("Price", cust_id)
            cust_data["formality"] = get_cust_pref("Formality", cust_id)
            cust_data["cuisine"] = get_cust_pref("Cuisine", cust_id)
            cust_data["diet"] = get_cust_pref("Diet_Category", cust_id, "Diet")

            return cust_data
        else:
            return "Invalid user id", 400
