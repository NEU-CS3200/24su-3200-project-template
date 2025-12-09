########
# Swapper endpoints
########

from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db
swapper = Blueprint('swapper', __name__)

#### ------------------------ Swapper------------------------
def SwapperNav():
    st.sidebar.page_link("pages/00_SwapperDash.py", label = "Swapper Home")

def SwapperFeed():
    st.sidebar.page_link("pages/50_Swapper_Feed.py", label = "Browse Feed", icon="👕" )

def SwapperSwaps():
    st.sidebar.page_link("pages/52_My_Swaps.py", label = "My Swaps", icon="🔄")



# ===========================================================================
# BROWSE FEED ROUTES
# User stories [1, 2, 3, 4]
# > As a Swapper, I want to be able to view items listed for swaps and filter them.
# > As a Swapper, I want to be able to upload clothing items as listings and list them as
#   for a swap or a take.
# > As a Swapper, I want to exchange my clothes I don't want anymore for other user’s clothes by
#   requesting a listing to swap in exchange for one of my pieces.
# ============================================================================
@swapper.route('/listings/filter_swaps', methods=['GET'])
def get_filter_listings():
    """
    Gets all listings that meet filter criteria AND sets filtering to
    be for swaps
    """
    category = request.args.get('category')
    size = request.args.get('size')
    condition = request.args.get('condition')
    tags = request.args.get('tags')
    user_id = request.args.get('user_id', type=int)

    cursor = db.get_db().cursor()

    the_query = '''
        SELECT DISTINCT
            i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name as OwnerName,
            i.ListedAt
        FROM Items i
        JOIN Users u ON i.OwnerID = u.UserID
        LEFT JOIN ItemTags it ON i.ItemID = it.ItemID
        LEFT JOIN Tags t ON it.TagID = t.TagID
        WHERE i.IsAvailable = 1 AND i.Type = 'swap'
    '''

    query_params = []
    # Exclude items owned by the current user
    if user_id:
        the_query += ' AND i.OwnerID != %s'
        query_params.append(user_id)

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

@swapper.route('/upload_listing/', methods=['POST'])
def upload_listing():
    """
    Posts listing for a specific user
    """
    try:
        cursor = db.get_db().cursor()
        data = request.get_json()

        title = data['Title']
        category = data['Category']
        description = data['Description']
        size = data['Size']
        item_type = data['Type']
        condition = data['Condition']
        owner_id = data['OwnerID']
        tags = data.get('Tags', [])  # Get tags, default to empty list

        the_query = '''
            INSERT INTO Items (Title, Category, Description, Size, `Type`, `Condition`, OwnerID, IsAvailable, ListedAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, NOW());
        '''

        cursor.execute(the_query, (title, category, description, size, item_type, condition, owner_id))
        item_id = cursor.lastrowid  # Get the ID of the inserted item

        # Handle tags if provided
        if tags:
            for tag_title in tags:
                # Check if tag exists, if not create it
                check_tag_query = 'SELECT TagID FROM Tags WHERE Title = %s'
                cursor.execute(check_tag_query, (tag_title,))
                tag_result = cursor.fetchone()

                if tag_result:
                    tag_id = tag_result['TagID']
                else:
                    # Create new tag
                    insert_tag_query = 'INSERT INTO Tags (Title) VALUES (%s)'
                    cursor.execute(insert_tag_query, (tag_title,))
                    tag_id = cursor.lastrowid

                # Link tag to item
                insert_item_tag_query = 'INSERT INTO ItemTags (ItemID, TagID) VALUES (%s, %s)'
                cursor.execute(insert_item_tag_query, (item_id, tag_id))

        db.get_db().commit()
        return make_response(jsonify({"message": "Listing uploaded successfully."}), 200)

    except Exception as e:
        db.get_db().rollback()
        the_response = make_response(jsonify({"error": str(e)}))
        the_response.status_code = 500
        return the_response


@swapper.route('/initiate_swap/', methods=['POST'])
def initiate_swap():
    """
    Posts a swap request after selecting specific listing
    """
    try:
        cursor = db.get_db().cursor()
        data = request.get_json()

        # Item they want (from another user)
        desired_item_id = data.get('desired_item_id')
        # Item they're offering (their own item)
        offered_item_id = data.get('offered_item_id')
        requester_id = data.get('requester_id')

        # Validate items exist and are available
        cursor.execute('''
            SELECT OwnerID, IsAvailable, Type
            FROM Items
            WHERE ItemID = %s
        ''', (desired_item_id,))
        desired_item = cursor.fetchone()

        if not desired_item or not desired_item['IsAvailable'] or desired_item['Type'] != 'swap':
            return make_response(jsonify({"error": "Desired item not available for swap"}), 400)

        owner_id = desired_item['OwnerID']

        if owner_id == requester_id:
            return make_response(jsonify({"error": "Cannot swap with yourself"}), 400)

        cursor.execute('''
            SELECT OwnerID, IsAvailable, Type
            FROM Items
            WHERE ItemID = %s
        ''', (offered_item_id,))
        offered_item = cursor.fetchone()

        if not offered_item or offered_item['OwnerID'] != requester_id or not offered_item['IsAvailable']:
            return make_response(jsonify({"error": "Offered item not available or not owned by you"}), 400)

        # Create swap order (requester is giving their item, receiving desired item)
        cursor.execute('''
            INSERT INTO Orders (GivenByID, ReceiverID, CreatedAt, ShippingID)
            VALUES (%s, %s, NOW(), NULL)
        ''', (requester_id, owner_id))
        order_id = cursor.lastrowid

        # Add both items to the order
        cursor.execute('''
            INSERT INTO OrderItems (OrderID, ItemID)
            VALUES (%s, %s)
        ''', (order_id, offered_item_id))

        cursor.execute('''
            INSERT INTO OrderItems (OrderID, ItemID)
            VALUES (%s, %s)
        ''', (order_id, desired_item_id))

        # Mark both items as unavailable
        cursor.execute('''
            UPDATE Items SET IsAvailable = 0 WHERE ItemID IN (%s, %s)
        ''', (offered_item_id, desired_item_id))

        db.get_db().commit()

        return make_response(jsonify({
            "message": "Swap request created successfully",
            "order_id": order_id
        }), 201)

    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@swapper.route('/my_items/<int:user_id>', methods=['GET'])
def get_my_items(user_id):
    """
    Gets all items owned by a user that are of type 'swap'
    """
    cursor = db.get_db().cursor()

    cursor.execute('''
        SELECT ItemID, Title, Category, Description, Size, `Condition`, IsAvailable, `Type`, ListedAt
        FROM Items
        WHERE OwnerID = %s AND `Type` = 'swap'
        ORDER BY ListedAt DESC
    ''', (user_id,))

    items = cursor.fetchall()

    # Get tags for all items
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

    # Add tags to each item
    for item in items:
        item_id = item['ItemID']
        item['Tags'] = ', '.join(tags_dict.get(item_id, []))

    return make_response(jsonify(items), 200)



# ===========================================================================
# MY SWAPS ROUTES
# User stories [2, 4, 5]
# > As a Swapper, I want to exchange my clothes I don't want anymore for other user’s clothes by
#   requesting a listing to swap in exchange for one of my pieces.
# > As a Swapper, I want to be able to cancel a swap and have my swapped clothing become available
#   again so that I can find another more suitable swap.
# > As a Swapper, I want to be able to track the status of my sending and receiving packages of my swap.
# ============================================================================
@swapper.route('/cancel_swap/<int:OrderID>/<int:UserID>/', methods=['DELETE'])
def cancel_swap(OrderID, UserID):
    """
    Deletes swap from a specific user
    """
    try:
        cursor = db.get_db().cursor()

        # Update items to be available again
        cursor.execute('''
            UPDATE Items i
            INNER JOIN OrderItems oi ON i.ItemID = oi.ItemID
            SET i.IsAvailable = 1
            WHERE oi.OrderID = %s
            AND i.OwnerID = %s;
        ''', (OrderID, UserID))
        
        # Delete related records
        cursor.execute("DELETE FROM Feedback WHERE OrderID = %s;", (OrderID,))
        cursor.execute("DELETE FROM OrderItems WHERE OrderID = %s;", (OrderID,))
        cursor.execute("DELETE FROM Orders WHERE OrderID = %s AND (GivenByID = %s OR ReceiverID = %s);", (OrderID, UserID, UserID))
        
        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Swap cancelled and item is now available for swap."}))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response

    except Exception as e:
        db.get_db().rollback()
        the_response = make_response(jsonify({"error": str(e)}))
        the_response.status_code = 500
        return the_response

@swapper.route('/track_swap/<int:UserID>/', methods=['GET'])
def track_swap(UserID):
    """
    Gets tracking information for all swaps of a user
    """
    cursor = db.get_db().cursor()

    the_query = '''
         SELECT
            o.OrderID,
            o.CreatedAt,
            CASE
                WHEN o.GivenByID = %s THEN 'Sending'
                WHEN o.ReceiverID = %s THEN 'Receiving'
            END AS SwapDirection,
            s.Carrier,
            s.TrackingNum,
            s.DateShipped,
            s.DateArrived,
            CASE
                WHEN s.DateArrived IS NOT NULL THEN 'Delivered'
                WHEN s.DateShipped IS NOT NULL THEN 'In Transit'
                ELSE 'Pending'
            END AS Status
        FROM Orders o
        LEFT JOIN Shippings s ON o.ShippingID = s.ShippingID
        WHERE o.GivenByID = %s OR o.ReceiverID = %s
        ORDER BY o.CreatedAt DESC;
    '''

    cursor.execute(the_query, (UserID, UserID, UserID, UserID))
    swaps = cursor.fetchall()

    # Get item details for each swap
    for swap in swaps:
        order_id = swap['OrderID']
        
        # Get all items in this swap
        items_query = '''
            SELECT 
                i.ItemID, i.Title, i.Category, i.Description, i.Size, i.`Condition`, i.OwnerID
            FROM OrderItems oi
            JOIN Items i ON oi.ItemID = i.ItemID
            WHERE oi.OrderID = %s
        '''
        cursor.execute(items_query, (order_id,))
        items = cursor.fetchall()
        
        # Determine which item is yours and which is theirs
        your_item = None
        their_item = None
        
        for item in items:
            if item['OwnerID'] == UserID:
                your_item = item
            else:
                their_item = item
        
        # Get tags for items
        item_ids = [item['ItemID'] for item in items]
        tags_dict = {}
        
        if item_ids:
            placeholders = ', '.join(['%s'] * len(item_ids))
            tags_query = f'''
                SELECT DISTINCT it.ItemID, t.Title
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
                # Only add tag if not already in list (prevent duplicates)
                if row['Title'] not in tags_dict[item_id]:
                    tags_dict[item_id].append(row['Title'])
        
        # Add tags to items
        if your_item:
            your_item['Tags'] = ', '.join(tags_dict.get(your_item['ItemID'], []))
        if their_item:
            their_item['Tags'] = ', '.join(tags_dict.get(their_item['ItemID'], []))
        
        # Add items to swap data
        swap['YourItem'] = your_item
        swap['TheirItem'] = their_item

    return make_response(jsonify(swaps), 200)



@swapper.route('/trades/ongoing/<int:user_id>', methods=['GET'])
def get_ongoing_trades(user_id):
    """
    Gets ongoing trades for user
    """
    cursor = db.get_db().cursor()
    # Get trades where user is either giving or receiving
    cursor.execute('''
        SELECT 
            o.OrderID as trade_id,
            CASE 
                WHEN o.GivenByID = %s THEN 'outgoing'
                WHEN o.ReceiverID = %s THEN 'incoming'
            END as type,
            CASE 
                WHEN o.GivenByID = %s THEN u2.Name
                WHEN o.ReceiverID = %s THEN u1.Name
            END as username,
            CASE 
                WHEN o.GivenByID = %s THEN u2.UserID
                WHEN o.ReceiverID = %s THEN u1.UserID
            END as other_user_id,
            'Pending' as status,
            NULL as location,
            NULL as date,
            NULL as your_item_img,
            NULL as their_item_img,
            0 as is_free
        FROM Orders o
        JOIN Users u1 ON o.GivenByID = u1.UserID
        JOIN Users u2 ON o.ReceiverID = u2.UserID
        LEFT JOIN Shippings s ON o.ShippingID = s.ShippingID
        WHERE (o.GivenByID = %s OR o.ReceiverID = %s)
        AND s.DateArrived IS NULL
        ORDER BY o.CreatedAt DESC
    ''', (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id))
    
    trades = cursor.fetchall()
    
    # Get items for each trade
    for trade in trades:
        cursor.execute('''
            SELECT i.ItemID, i.Title, img.ImageURL
            FROM OrderItems oi
            JOIN Items i ON oi.ItemID = i.ItemID
            LEFT JOIN Images img ON i.ItemID = img.ItemID AND img.ImageOrderNum = 1
            WHERE oi.OrderID = %s
        ''', (trade['trade_id'],))
        items = cursor.fetchall()
        
        # Determine which item is yours and which is theirs
        for item in items:
            cursor.execute('SELECT OwnerID FROM Items WHERE ItemID = %s', (item['ItemID'],))
            owner = cursor.fetchone()
            if owner['OwnerID'] == user_id:
                trade['your_item_img'] = item.get('ImageURL')
            else:
                trade['their_item_img'] = item.get('ImageURL')
    
    return make_response(jsonify(trades), 200)

# Get completed trades for a user
@swapper.route('/trades/completed/<int:user_id>', methods=['GET'])
def get_completed_trades(user_id):
    """
    Gets completed trades
    """
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT 
            o.OrderID as trade_id,
            CASE 
                WHEN o.GivenByID = %s THEN u2.Name
                WHEN o.ReceiverID = %s THEN u1.Name
            END as username,
            s.DateArrived as completed_date,
            NULL as location,
            NULL as your_item_img,
            NULL as their_item_img
        FROM Orders o
        JOIN Users u1 ON o.GivenByID = u1.UserID
        JOIN Users u2 ON o.ReceiverID = u2.UserID
        JOIN Shippings s ON o.ShippingID = s.ShippingID
        WHERE (o.GivenByID = %s OR o.ReceiverID = %s)
        AND s.DateArrived IS NOT NULL
        ORDER BY s.DateArrived DESC
    ''', (user_id, user_id, user_id, user_id))
    
    trades = cursor.fetchall()
    
    # Get items for each trade
    for trade in trades:
        cursor.execute('''
            SELECT i.ItemID, img.ImageURL
            FROM OrderItems oi
            JOIN Items i ON oi.ItemID = i.ItemID
            LEFT JOIN Images img ON i.ItemID = img.ItemID AND img.ImageOrderNum = 1
            WHERE oi.OrderID = %s
        ''', (trade['trade_id'],))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute('SELECT OwnerID FROM Items WHERE ItemID = %s', (item['ItemID'],))
            owner = cursor.fetchone()
            if owner['OwnerID'] == user_id:
                trade['your_item_img'] = item.get('ImageURL')
            else:
                trade['their_item_img'] = item.get('ImageURL')
    
    return make_response(jsonify(trades), 200)


@swapper.route('/trades/<int:trade_id>/accept', methods=['PUT'])
def accept_trade(trade_id):
    """
    Allows user to accept a swap request
    """
    try:
        cursor = db.get_db().cursor()
        user_id = request.args.get('user_id', type=int)
        
        # Verify user is the receiver
        cursor.execute('''
            SELECT ReceiverID FROM Orders WHERE OrderID = %s
        ''', (trade_id,))
        order = cursor.fetchone()
        
        if not order or order['ReceiverID'] != user_id:
            return make_response(jsonify({"error": "Unauthorized"}), 403)
        
        # Create shipping records for both items (simplified - in real app would need separate shippings)
        # For now, just mark as accepted by creating a shipping record
        cursor.execute('''
            INSERT INTO Shippings (Carrier, TrackingNum, DateShipped, DateArrived)
            VALUES ('Pending', 'TBD', CURDATE(), NULL)
        ''')
        shipping_id = cursor.lastrowid
        
        cursor.execute('''
            UPDATE Orders SET ShippingID = %s WHERE OrderID = %s
        ''', (shipping_id, trade_id))
        
        db.get_db().commit()
        
        return make_response(jsonify({"message": "Trade accepted"}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@swapper.route('/trades/<int:trade_id>/reject', methods=['PUT'])
def reject_trade(trade_id):
    """
    Allows user to reject a trade
    """
    try:
        cursor = db.get_db().cursor()
        user_id = request.args.get('user_id', type=int)
        
        # Verify user is the receiver
        cursor.execute('''
            SELECT ReceiverID FROM Orders WHERE OrderID = %s
        ''', (trade_id,))
        order = cursor.fetchone()
        
        if not order or order['ReceiverID'] != user_id:
            return make_response(jsonify({"error": "Unauthorized"}), 403)
        
        # Get items in the order and make them available again
        cursor.execute('''
            SELECT ItemID FROM OrderItems WHERE OrderID = %s
        ''', (trade_id,))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute('''
                UPDATE Items SET IsAvailable = 1 WHERE ItemID = %s
            ''', (item['ItemID'],))
        
        # Delete order items and order
        cursor.execute('DELETE FROM OrderItems WHERE OrderID = %s', (trade_id,))
        cursor.execute('DELETE FROM Orders WHERE OrderID = %s', (trade_id,))
        
        db.get_db().commit()
        
        return make_response(jsonify({"message": "Trade rejected"}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@swapper.route('/trades/<int:trade_id>/cancel', methods=['PUT'])
def cancel_trade(trade_id):
    """
    Allows initiator user to cancel a trade
    """
    try:
        cursor = db.get_db().cursor()
        user_id = request.args.get('user_id', type=int)
        
        # Verify user is the initiator (GivenByID)
        cursor.execute('''
            SELECT GivenByID FROM Orders WHERE OrderID = %s
        ''', (trade_id,))
        order = cursor.fetchone()
        
        if not order or order['GivenByID'] != user_id:
            return make_response(jsonify({"error": "Unauthorized"}), 403)
        
        # Get items and make them available again
        cursor.execute('''
            SELECT ItemID FROM OrderItems WHERE OrderID = %s
        ''', (trade_id,))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute('''
                UPDATE Items SET IsAvailable = 1 WHERE ItemID = %s
            ''', (item['ItemID'],))
        
        # Delete order items and order
        cursor.execute('DELETE FROM OrderItems WHERE OrderID = %s', (trade_id,))
        cursor.execute('DELETE FROM Orders WHERE OrderID = %s', (trade_id,))
        
        db.get_db().commit()
        
        return make_response(jsonify({"message": "Trade cancelled"}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({"error": str(e)}), 500)


