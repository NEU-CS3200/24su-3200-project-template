########
# Taker endpoints
########

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

taker = Blueprint('taker', __name__)

# ===========================================================================
# BROWSE FEED ROUTES
# User stories [1, 2]
# > As a Taker, I want to see clothes that are listed for take and filter by size, condition,
#   and style, so I can find items that suit me.
# > [NEW] As a Taker, I want to be able to select an item for takes.
# ===========================================================================
@taker.route('/listings/filter_takes', methods=['GET'])
def get_filter_listings():
    """
    Get listings that meet filter requirements and are takes
    """
    category = request.args.get('category')
    size = request.args.get('size')
    condition = request.args.get('condition')
    tags = request.args.get('tags')

    cursor = db.get_db().cursor()

    the_query = '''
        SELECT DISTINCT
            i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name as OwnerName,
            i.ListedAt
        FROM Items i
        JOIN Users u ON i.OwnerID = u.UserID
        LEFT JOIN ItemTags it ON i.ItemID = it.ItemID
        LEFT JOIN Tags t ON it.TagID = t.TagID
        WHERE i.IsAvailable = 1 AND i.Type = 'take'
    '''

    query_params = []

    if category:
        the_query += ' AND i.Category = %s'
        query_params.append(category)

    if size:
        the_query += ' AND i.Size = %s'
        query_params.append(size)

    if condition:
        conditions = condition.split(',')
        placeholders = ', '.join(['%s'] * len(conditions))
        the_query += f' AND i.Condition IN ({placeholders})'
        query_params.extend(conditions)

    if tags:
        tag_list = tags.split(',')
        placeholders = ', '.join(['%s'] * len(tag_list))
        the_query += f' AND t.Title IN ({placeholders}) OR t.Title IS NULL'
        query_params.extend(tag_list)

    the_query += ' ORDER BY i.ListedAt DESC;'

    cursor.execute(the_query, query_params)
    items = cursor.fetchall()

    item_ids = [item['ItemID'] for item in items]
    tags_dict = {}
    
    if item_ids:
        placeholders = ', '.join(['%s'] * len(item_ids))
        tags_query = f'''
            SELECT it.ItemID, t.Title
            FROM ItemTags it
            JOIN Tags t ON it.TagID = t.TagID
            WHERE it.ItemID IN ({placeholders})
        '''
        cursor.execute(tags_query, item_ids)
        tag_rows = cursor.fetchall()
        
        for row in tag_rows:
            item_id = row['ItemID']
            if item_id not in tags_dict:
                tags_dict[item_id] = []
            tags_dict[item_id].append(row['Title'])

    for item in items:
        item_id = item['ItemID']
        item['Tags'] = ', '.join(tags_dict.get(item_id, []))

    the_response = make_response(jsonify(items), 200)
    the_response.mimetype = "application/json"
    return the_response

@taker.route('/request_item', methods=['POST'])
def request_item():
    """
    Post Take request, different from posting swap request as
    it does not need to reincorporated
    """
    data = request.get_json()
    item_id = data.get('item_id')
    user_id = data.get('user_id')

    cursor = db.get_db().cursor()

    the_query = '''
        SELECT OwnerID
        FROM Items
        WHERE ItemID = %s AND IsAvailable = 1
    '''
    cursor.execute(the_query, (item_id,))
    item = cursor.fetchone()

    if not item:
        the_response = make_response(jsonify({"message": "Item not found or not available"}), 404)
        the_response.mimetype = "application/json"
        return the_response

    owner_id = item['OwnerID']

    the_query = '''
        INSERT INTO Orders (GivenByID, ReceiverID, CreatedAt, ShippingID)
        VALUES (%s, %s, NOW(), NULL)
    '''
    cursor.execute(the_query, (owner_id, user_id))
    order_id = cursor.lastrowid

    the_query = '''
        INSERT INTO OrderItems (OrderID, ItemID)
        VALUES (%s, %s)
    '''
    cursor.execute(the_query, (order_id, item_id))

    the_query = '''
        UPDATE Items
        SET IsAvailable = 0
        WHERE ItemID = %s
    '''
    cursor.execute(the_query, (item_id,))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Item requested successfully"}), 201)
    the_response.mimetype = "application/json"
    return the_response



# ===========================================================================
# View My Orders
# User stories [3, 4]
# > As a Taker, I want to be able to track the status of my incoming package.
# > [NEW] As a Taker, I want to be able to cancel my taker request.
# ===========================================================================
@taker.route('/check_request/<int:user_id>/<int:item_id>', methods=['GET'])
def check_request(user_id, item_id):
    """
    Gets status of selected item
    """
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT o.OrderID
        FROM Orders o
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        WHERE o.ReceiverID = %s
          AND oi.ItemID = %s
          AND o.ShippingID IS NULL
    '''
    cursor.execute(the_query, (user_id, item_id))
    result = cursor.fetchone()

    if result:
        order_id = result['OrderID']
        the_response = make_response(jsonify({"requested": True, "order_id": order_id}), 200)
    else:
        the_response = make_response(jsonify({"requested": False}), 200)
    
    the_response.mimetype = "application/json"
    return the_response

@taker.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_take_request(order_id):
    """
    Delete take request for specific take, different from deleting swap
    request as it can not go two ways
   """
    user_id = request.args.get('user_id')

    cursor = db.get_db().cursor()

    the_query = '''
        SELECT oi.ItemID
        FROM OrderItems oi
        JOIN Orders o ON oi.OrderID = o.OrderID
        WHERE oi.OrderID = %s
          AND o.ReceiverID = %s
          AND o.ShippingID IS NULL
    '''
    cursor.execute(the_query, (order_id, user_id))
    item_result = cursor.fetchone()

    if not item_result:
        the_response = make_response(jsonify({"message": "No matching take request found."}), 404)
        the_response.mimetype = "application/json"
        return the_response

    item_id = item_result['ItemID']

    the_query = '''
        DELETE FROM OrderItems
        WHERE OrderID = %s
    '''
    cursor.execute(the_query, (order_id,))

    the_query = '''
        DELETE FROM Orders
        WHERE OrderID = %s
    '''
    cursor.execute(the_query, (order_id,))

    the_query = '''
        UPDATE Items
        SET IsAvailable = 1
        WHERE ItemID = %s
    '''
    cursor.execute(the_query, (item_id,))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Take request canceled successfully."}), 200)
    the_response.mimetype = "application/json"
    return the_response

@taker.route('/track_package/<int:user_id>', methods=['GET'])
def track_package(user_id):
    """
    Gets tracking status of a selected item
    """
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            o.OrderID, i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition,
            o.CreatedAt as RequestDate, s.Carrier, s.TrackingNum, s.DateShipped, s.DateArrived
        FROM Orders o
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Items i ON oi.ItemID = i.ItemID
        LEFT JOIN Shippings s ON o.ShippingID = s.ShippingID
        WHERE o.ReceiverID = %s
        ORDER BY o.CreatedAt DESC;
    '''

    cursor.execute(the_query, (user_id,))
    orders = cursor.fetchall()

    if orders:
        item_ids = [order['ItemID'] for order in orders]
        tags_dict = {}

        if item_ids:
            placeholders = ', '.join(['%s'] * len(item_ids))
            tags_query = f'''
                SELECT it.ItemID, t.Title
                FROM ItemTags it
                JOIN Tags t ON it.TagID = t.TagID
                WHERE it.ItemID IN ({placeholders})
            '''
            cursor.execute(tags_query, item_ids)
            tag_rows = cursor.fetchall()

            for row in tag_rows:
                item_id = row['ItemID']
                if item_id not in tags_dict:
                    tags_dict[item_id] = []
                tags_dict[item_id].append(row['Title'])

        for order in orders:
            item_id = order['ItemID']
            order['Tags'] = ', '.join(tags_dict.get(item_id, []))

    the_response = make_response(jsonify(orders if orders else []), 200)
    the_response.mimetype = "application/json"
    return the_response



# ===========================================================================
# RECOMMENDATIONS ROUTES
# User stories [6]
# >[NEW] As a Taker, I want to be able to get recommendations, based on past order history.
# ===========================================================================
@taker.route('/recommendations/<int:taker_id>', methods=['GET'])
def get_recommendations(taker_id):
    """
    Gets recommendation for selected users based on past suer history.
    """
    cursor = db.get_db().cursor()

    check_orders_query = '''
        SELECT COUNT(*) as order_count
        FROM Orders
        WHERE ReceiverID = %s
    '''
    cursor.execute(check_orders_query, (taker_id,))
    order_check = cursor.fetchone()
    has_orders = order_check['order_count'] > 0 if order_check else False

    if has_orders:
        user_categories_query = '''
            SELECT DISTINCT i2.Category
            FROM Items i2
            JOIN OrderItems oi2 ON i2.ItemID = oi2.ItemID
            JOIN Orders o2 ON oi2.OrderID = o2.OrderID
            WHERE o2.ReceiverID = %s
        '''
        cursor.execute(user_categories_query, (taker_id,))
        user_categories = [row['Category'] for row in cursor.fetchall()]

        user_sizes_query = '''
            SELECT DISTINCT i3.Size
            FROM Items i3
            JOIN OrderItems oi3 ON i3.ItemID = oi3.ItemID
            JOIN Orders o3 ON oi3.OrderID = o3.OrderID
            WHERE o3.ReceiverID = %s
        '''
        cursor.execute(user_sizes_query, (taker_id,))
        user_sizes = [row['Size'] for row in cursor.fetchall()]

        user_tags_query = '''
            SELECT t.TagID, t.Title, COUNT(*) as tag_count
            FROM Tags t
            JOIN ItemTags it ON t.TagID = it.TagID
            JOIN Items i ON it.ItemID = i.ItemID
            JOIN OrderItems oi ON i.ItemID = oi.ItemID
            JOIN Orders o ON oi.OrderID = o.OrderID
            WHERE o.ReceiverID = %s
            GROUP BY t.TagID, t.Title
            ORDER BY tag_count DESC
            LIMIT 5
        '''
        cursor.execute(user_tags_query, (taker_id,))
        user_tag_rows = cursor.fetchall()
        user_tag_ids = [row['TagID'] for row in user_tag_rows]
        user_style_prefs = [row['Title'] for row in user_tag_rows]

        requested_items_query = '''
            SELECT oi.ItemID
            FROM OrderItems oi
            JOIN Orders o ON oi.OrderID = o.OrderID
            WHERE o.ReceiverID = %s
        '''
        cursor.execute(requested_items_query, (taker_id,))
        requested_item_ids = [row['ItemID'] for row in cursor.fetchall()]

        if requested_item_ids:
            requested_items_str = ','.join(map(str, requested_item_ids))
            exclude_clause = f"AND i.ItemID NOT IN ({requested_items_str})"
        else:
            exclude_clause = ""

        category_match = "i.Category IN (" + ",".join([f"'{cat}'" for cat in user_categories]) + ")" if user_categories else "0=1"
        size_match = "i.Size IN (" + ",".join([f"'{s}'" for s in user_sizes]) + ")" if user_sizes else "0=1"
        
        if user_tag_ids:
            tags_str = ','.join(map(str, user_tag_ids))
            style_match = f"EXISTS (SELECT 1 FROM ItemTags it2 WHERE it2.ItemID = i.ItemID AND it2.TagID IN ({tags_str}))"
        else:
            style_match = "0=1"

        the_query = f'''
            SELECT
                i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name as OwnerName, i.ListedAt,
                CASE WHEN {category_match} THEN 1 ELSE 0 END as MatchesCategory,
                CASE WHEN {size_match} THEN 1 ELSE 0 END as MatchesSize,
                CASE WHEN {style_match} THEN 1 ELSE 0 END as MatchesStyle,
                CASE
                    WHEN {category_match} AND {size_match} AND {style_match} THEN 3
                    WHEN ({category_match} AND {size_match}) OR ({category_match} AND {style_match}) OR ({size_match} AND {style_match}) THEN 2
                    WHEN {category_match} OR {size_match} OR {style_match} THEN 1
                    ELSE 0
                END as MatchScore
            FROM Items i
            JOIN Users u ON i.OwnerID = u.UserID
            WHERE i.IsAvailable = 1
              AND i.Type = 'take'
              {exclude_clause}
              AND ({category_match} OR {size_match} OR {style_match})
            ORDER BY MatchScore DESC, i.ListedAt DESC
            LIMIT 3;
        '''
        cursor.execute(the_query)
        items = cursor.fetchall()

        item_ids = [item['ItemID'] for item in items]
        tags_dict = {}
        
        if item_ids:
            placeholders = ', '.join(['%s'] * len(item_ids))
            tags_query = f'''
                SELECT it.ItemID, t.Title
                FROM ItemTags it
                JOIN Tags t ON it.TagID = t.TagID
                WHERE it.ItemID IN ({placeholders})
            '''
            cursor.execute(tags_query, item_ids)
            tag_rows = cursor.fetchall()
            
            for row in tag_rows:
                item_id = row['ItemID']
                if item_id not in tags_dict:
                    tags_dict[item_id] = []
                tags_dict[item_id].append(row['Title'])

        for item in items:
            item_id = item['ItemID']
            item['Tags'] = ', '.join(tags_dict.get(item_id, []))

        for item in items:
            matches_category = item['MatchesCategory'] == 1
            matches_size = item['MatchesSize'] == 1
            matches_style = item['MatchesStyle'] == 1

            item_tags = []
            if item.get('Tags'):
                item_tags = [tag.strip() for tag in item['Tags'].split(',')]
            
            matching_styles = list(set([pref for pref in user_style_prefs if pref in item_tags]))
            
            reason_parts = []
            if matches_category and matches_size and matches_style:
                reason_parts.append(f"Perfect match! Matches your category ({item['Category']}), size ({item['Size']})")
                if matching_styles:
                    style_list = ', '.join(matching_styles)
                    reason_parts.append(f"and style preferences ({style_list})")
                item['RecommendationReason'] = ' '.join(reason_parts)
            elif matches_category and matches_size:
                item['RecommendationReason'] = f"Matches your category ({item['Category']}) and size ({item['Size']})"
            elif matches_category and matches_style:
                if matching_styles:
                    style_list = ', '.join(matching_styles)
                    item['RecommendationReason'] = f"Matches your category ({item['Category']}) and style preferences ({style_list})"
                else:
                    item['RecommendationReason'] = f"Matches your category ({item['Category']}) and style preferences"
            elif matches_size and matches_style:
                if matching_styles:
                    style_list = ', '.join(matching_styles)
                    item['RecommendationReason'] = f"Matches your size ({item['Size']}) and style preferences ({style_list})"
                else:
                    item['RecommendationReason'] = f"Matches your size ({item['Size']}) and style preferences"
            elif matches_category:
                item['RecommendationReason'] = f"Matches your category: {item['Category']}"
            elif matches_size:
                item['RecommendationReason'] = f"Matches your size: {item['Size']}"
            elif matches_style:
                if matching_styles:
                    style_list = ', '.join(matching_styles)
                    item['RecommendationReason'] = f"Matches your style preferences: {style_list}"
                else:
                    item['RecommendationReason'] = "Matches your style preferences"
            else:
                item['RecommendationReason'] = 'Recommended for you'

            del item['MatchesCategory']
            del item['MatchesSize']
            del item['MatchesStyle']

        theData = items
    else:
        the_query = '''
            SELECT
                i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name as OwnerName, i.ListedAt,
                'New user: showing recently listed items' as RecommendationReason
            FROM Items i
            JOIN Users u ON i.OwnerID = u.UserID
            WHERE i.IsAvailable = 1
              AND i.Type = 'take'
            ORDER BY i.ListedAt DESC
            LIMIT 3;
        '''
        cursor.execute(the_query)
        items = cursor.fetchall()

        item_ids = [item['ItemID'] for item in items]
        tags_dict = {}
        
        if item_ids:
            placeholders = ', '.join(['%s'] * len(item_ids))
            tags_query = f'''
                SELECT it.ItemID, t.Title
                FROM ItemTags it
                JOIN Tags t ON it.TagID = t.TagID
                WHERE it.ItemID IN ({placeholders})
            '''
            cursor.execute(tags_query, item_ids)
            tag_rows = cursor.fetchall()
            
            for row in tag_rows:
                item_id = row['ItemID']
                if item_id not in tags_dict:
                    tags_dict[item_id] = []
                tags_dict[item_id].append(row['Title'])

        for item in items:
            item_id = item['ItemID']
            item['Tags'] = ', '.join(tags_dict.get(item_id, []))

        theData = items
    the_response = make_response(jsonify(theData), 200)
    the_response.mimetype = "application/json"
    return the_response

