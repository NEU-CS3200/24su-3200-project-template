from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# New Blueprint for applications
views_position = Blueprint('views_position', __name__)

# student flags positions they like/do not like 
@views_position.route('/position', methods=['POST'])
def set_job_preference():
    the_data = request.json
    current_app.logger.info(the_data)
    
    student_id = the_data['studentId']
    coop_position_id = the_data['coopPositionId']
    preference = the_data['preference']  
    
    query = f'''
        INSERT INTO viewsPos (studentId, coopPositionId, preference)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE preference = VALUES(preference)
    '''
    current_app.logger.info(query)
    
    # Execute query and commit
    cursor = db.get_db().cursor()
    cursor.execute(query, (student_id, coop_position_id, int(preference)))
    db.get_db().commit()
    
    # Return success response
    response = make_response("Preference saved successfully")
    response.status_code = 200
    return response

# student deletes preference for a posting 
@views_position.route('/position', methods=['DELETE'])
def remove_job_preference():
    the_data = request.json
    current_app.logger.info(f"DELETE preference for: {the_data}")
    
    student_id = the_data['studentId']
    coop_position_id = the_data['coopPositionId']

    query = '''
        DELETE FROM viewsPos
        WHERE studentId = %s AND coopPositionId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (student_id, coop_position_id))
    db.get_db().commit()

    return make_response(jsonify({"message": "Preference removed"}), 200)


# Student views deadlines for positions
@views_position.route('/<int:studentID>/deadlines', methods=['GET'])
def get_deadlines(studentID):
    current_app.logger.info(f'GET /{studentID}/deadlines route')

    query = '''
        SELECT cp.title,
            cp.deadline
        FROM viewsPos vp
            JOIN coopPositions cp ON vp.coopPositionId = cp.coopPositionId
        WHERE vp.studentId = %s AND vp.preference = TRUE;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (studentID,))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Student views positions based on preference
@views_position.route('/viewpos/<int:studentID>', methods=['GET'])
def get_positions_by_preference(studentID):
    current_app.logger.info(f'GET /viewpos/{studentID} route')

    pref_param = request.args.get('preference')

    # Validate preference query param and build SQL condition
    preference_clause = ''
    if pref_param is not None:
        if pref_param.lower() in ['true', '1']:
            preference_clause = 'AND vp.preference = TRUE'
        elif pref_param.lower() in ['false', '0']:
            preference_clause = 'AND vp.preference = FALSE'
        else:
            return jsonify({"error": "Invalid preference value"}), 400

    query = f'''
        SELECT cp.*
        FROM viewsPos vp
        JOIN coopPositions cp ON cp.coopPositionId = vp.coopPositionId
        WHERE vp.studentId = %s
        {preference_clause}
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentID,))
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching positions by preference: {e}")
        return jsonify({"error": "Server error"}), 500
    

# Admin views preference metrics 
@views_position.route('/viewspos/<int:preference>', methods=['GET'])
def get_preference_metrics(preference):
    current_app.logger.info('GET /viewspos/%s route', preference)

    query = '''
        SELECT
            cp.coopPositionId,
            cp.title,
            com.name AS companyName,
            COUNT(vp.studentId) AS prefCount
        FROM coopPositions cp
        LEFT JOIN createsPos cr
          ON cr.coopPositionId = cp.coopPositionId
        LEFT JOIN users u
          ON u.userId = cr.employerId
        LEFT JOIN companyProfiles com
          ON com.companyProfileId = u.companyProfileId
        LEFT JOIN viewsPos vp
          ON vp.coopPositionId = cp.coopPositionId
         AND vp.preference = %s
        GROUP BY cp.coopPositionId, cp.title, com.name
        ORDER BY prefCount DESC, cp.title ASC;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (preference,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response