from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

coopPositions = Blueprint('coopPositions', __name__)

#Student views a co-op position
@coopPositions.route('/positions', methods = ['GET'])
def get_position_info():
    current_app.logger.info('GET /positions route')
    query = '''
        SELECT cp.*
        FROM coopPositions cp
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Student/Advisor views the average pay for each industry
@coopPositions.route('/coopPositions/industryAveragePay', methods=['GET'])
def get_industry_average_pay():
    query = '''
        SELECT cp.industry, AVG(cp.hourlyPay) AS industryAvgHourlyPay
        FROM coopPositions cp
        GROUP BY cp.industry;
        '''
    
    current_app.logger.info('GET /industryAveragePay route')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Student view positions with desired skills that match their skills
@coopPositions.route('/<int:studentID>/desiredSkills', methods=['GET'])
def get_desired_skills(studentID):
    current_app.logger.info('GET /desiredSkills route')

    query = '''
        SELECT cp.coopPositionId,
            cp.title,
            cp.location,
            cp.description
        FROM coopPositions cp
            LEFT JOIN viewsPos vp ON cp.coopPositionId = vp.coopPositionId
            JOIN users u ON u.userId = %s
        WHERE (vp.preference IS NULL OR vp.preference = TRUE)
            AND cp.desiredSkillsId IN (SELECT skillId
                                        FROM skillDetails
                                        WHERE studentId = %s)
            AND (cp.desiredGPA IS NULL OR cp.desiredGPA <= u.grade)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (studentID, studentID))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# students view positions with required skills that match their skills 
@coopPositions.route('/<int:studentID>/requiredSkills', methods=['GET'])
def get_required_skills(studentID):
    current_app.logger.info('GET /requiredSkills route')

    query = '''
        SELECT cp.coopPositionId,
            cp.title,
            cp.location,
            cp.description
        FROM coopPositions cp
            LEFT JOIN viewsPos vp ON cp.coopPositionId = vp.coopPositionId
            JOIN users u ON u.userId = %s
        WHERE (vp.preference IS NULL OR vp.preference = TRUE)
            AND cp.requiredSkillsId IN (SELECT skillId
                                        FROM skillDetails
                                        WHERE studentId = %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (studentID, studentID))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Employer posts co-op position
@coopPositions.route('/createsPos/coopPosition', methods=['POST'])
def create_position():
    current_app.logger.info('POST /createsPos/coopPosition')

    try:
        pos_info = request.json
        current_app.logger.info(f"Received position data: {pos_info}")

        # Extract data without trailing commas (which create tuples)
        coop_position_id = pos_info['coopPositionId']
        title = pos_info['title']
        location = pos_info['location']
        description = pos_info['description']
        hourly_pay = pos_info['hourlyPay']
        required_skills = pos_info.get('requiredSkillsId')
        desired_skills = pos_info.get('desiredSkillsId')
        desired_gpa = pos_info.get('desiredGPA')
        deadline = pos_info.get('deadline')
        start_date = pos_info['startDate']
        end_date = pos_info['endDate']
        flag = pos_info.get('flag', False)  # Use 'flag' instead of 'flagged'
        industry = pos_info['industry']

        # Check if position ID already exists to prevent duplicates
        cursor = db.get_db().cursor()
        check_query = '''
            SELECT coopPositionId FROM coopPositions WHERE coopPositionId = %s
        '''
        cursor.execute(check_query, (coop_position_id,))

        if cursor.fetchone():
            current_app.logger.error(f"Position ID {coop_position_id} already exists")
            return make_response(jsonify({
                "error": f"Position ID {coop_position_id} already exists. Please refresh and try again."
            }), 409)

        # Use correct column name 'flag' instead of 'flagged'
        query = '''
            INSERT INTO coopPositions
                (coopPositionId, title, location, description, hourlyPay, requiredSkillsId,
                 desiredSkillsId, desiredGPA, deadline, startDate, endDate, flag, industry)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        data = (coop_position_id, title, location, description, hourly_pay,
                required_skills, desired_skills, desired_gpa, deadline, start_date,
                end_date, flag, industry)

        cursor.execute(query, data)
        db.get_db().commit()

        current_app.logger.info(f"Successfully created position {coop_position_id}")
        return make_response(jsonify({
            "message": "Position created!",
            "coopPositionId": coop_position_id
        }), 201)

    except Exception as e:
        current_app.logger.error(f"Error creating position: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# Link employer to position (createsPos relationship)
@coopPositions.route('/createsPos', methods=['POST'])
def link_employer_to_position():
    current_app.logger.info('POST /createsPos')

    try:
        link_info = request.json
        current_app.logger.info(f"Received link data: {link_info}")

        employer_id = link_info['employerId']
        coop_position_id = link_info['coopPositionId']

        # Check if the position exists
        check_query = '''
            SELECT coopPositionId FROM coopPositions WHERE coopPositionId = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(check_query, (coop_position_id,))

        if not cursor.fetchone():
            return make_response(jsonify({"error": f"Position {coop_position_id} not found"}), 404)

        # Insert the relationship
        query = '''
            INSERT INTO createsPos (employerId, coopPositionId)
            VALUES (%s, %s)
        '''

        cursor.execute(query, (employer_id, coop_position_id))
        db.get_db().commit()

        current_app.logger.info(f"Successfully linked employer {employer_id} to position {coop_position_id}")
        return make_response(jsonify({
            "message": "Employer linked to position!",
            "employerId": employer_id,
            "coopPositionId": coop_position_id
        }), 201)

    except Exception as e:
        current_app.logger.error(f"Error linking employer to position: {e}")
        return make_response(jsonify({"error": str(e)}), 500)



# Admin reviews all positions (both pending and approved)
@coopPositions.route('/coopPositions/pending', methods=['GET'])
def get_all_positions_for_admin():
    current_app.logger.info('GET /pending route')

    query = '''
        SELECT
            cp.coopPositionId,
            cp.title,
            cp.location,
            cp.description,
            cp.hourlyPay,
            cp.deadline,
            cp.startDate,
            cp.endDate,
            cp.industry,
            cp.flag,
            com.name AS companyName
        FROM coopPositions cp
        LEFT JOIN createsPos cr  ON cr.coopPositionId = cp.coopPositionId
        LEFT JOIN users u        ON u.userId = cr.employerId
        LEFT JOIN companyProfiles com ON com.companyProfileId = u.companyProfileId
        ORDER BY cp.flag DESC, cp.deadline IS NULL, cp.deadline ASC, cp.coopPositionId DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Admin views number of co-ops posted by each employer
@coopPositions.route('/coopPositions/employerJobCounts', methods=['GET'])
def get_employer_job_counts():
    current_app.logger.info('GET /employerJobCounts route')

    query = '''
        SELECT
            u.userId AS employerId,
            u.firstName,
            u.lastName,
            com.name AS companyName,
            COUNT(cr.coopPositionId) AS numJobs
        FROM users u
        JOIN companyProfiles com
            ON com.companyProfileId = u.companyProfileId
        LEFT JOIN createsPos cr
            ON cr.employerId = u.userId
        WHERE u.companyProfileId IS NOT NULL 
        GROUP BY u.userId, u.firstName, u.lastName, com.name
        ORDER BY numJobs DESC, u.lastName ASC, u.firstName ASC;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Admin approves a co-op position
@coopPositions.route('/coopPositions/<int:pos_id>/approve', methods=['PUT'])
def approve_position(pos_id):
    current_app.logger.info('PUT /coopPositions/%s/approve route', pos_id)

    # First check if the position exists
    check_query = '''
        SELECT coopPositionId, flag
        FROM coopPositions
        WHERE coopPositionId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(check_query, (pos_id,))
    position = cursor.fetchone()

    if not position:
        the_response = make_response(jsonify({
            "ok": False,
            "error": f"Position {pos_id} not found"
        }))
        the_response.status_code = 404
        return the_response

    # Check if already approved
    if position['flag'] == 0:  # flag = FALSE means already approved
        the_response = make_response(jsonify({
            "ok": True,
            "positionId": pos_id,
            "status": "already approved",
            "message": f"Position {pos_id} is already approved"
        }))
        the_response.status_code = 200
        return the_response

    # Approve the position (set flag to FALSE)
    update_query = '''
        UPDATE coopPositions
        SET flag = FALSE
        WHERE coopPositionId = %s
    '''

    cursor.execute(update_query, (pos_id,))
    db.get_db().commit()

    the_response = make_response(jsonify({
        "ok": True,
        "positionId": pos_id,
        "status": "approved",
        "message": f"Position {pos_id} has been approved"
    }))
    the_response.status_code = 200
    return the_response

# Admin deletes a co-op position
@coopPositions.route('/coopPositions/<int:pos_id>', methods=['DELETE'])
def delete_position(pos_id):
    current_app.logger.info('DELETE /coopPositions/%s route', pos_id)

    # First check if the position exists
    check_query = '''
        SELECT coopPositionId, flag, title
        FROM coopPositions
        WHERE coopPositionId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(check_query, (pos_id,))
    position = cursor.fetchone()

    if not position:
        the_response = make_response(jsonify({
            "ok": False,
            "error": f"Position {pos_id} not found"
        }))
        the_response.status_code = 404
        return the_response

    # Delete the position (remove flag restriction for admin flexibility)
    delete_query = '''
        DELETE FROM coopPositions
        WHERE coopPositionId = %s
    '''

    try:
        cursor.execute(delete_query, (pos_id,))
        db.get_db().commit()

        the_response = make_response(jsonify({
            "ok": True,
            "positionId": pos_id,
            "deleted": True,
            "message": f"Position {pos_id} '{position['title']}' has been permanently deleted"
        }))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        current_app.logger.error(f"Error deleting position {pos_id}: {e}")
        the_response = make_response(jsonify({
            "ok": False,
            "error": f"Cannot delete position {pos_id} due to related records (applications, etc.)"
        }))
        the_response.status_code = 409
        return the_response
    
# Admin flags a position
@coopPositions.route('/coopPositions/<int:pos_id>/flag/<int:value>', methods=['PUT'])
def set_position_flag(pos_id, value):
    current_app.logger.info('PUT /coopPositions/%s/flag/%s route', pos_id, value)

    # First check if the position exists
    check_query = '''
        SELECT coopPositionId, flag
        FROM coopPositions
        WHERE coopPositionId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(check_query, (pos_id,))
    position = cursor.fetchone()

    if not position:
        the_response = make_response(jsonify({
            "ok": False,
            "error": f"Position {pos_id} not found"
        }))
        the_response.status_code = 404
        return the_response

    # Validate flag value (should be 0 or 1)
    if value not in [0, 1]:
        the_response = make_response(jsonify({
            "ok": False,
            "error": "Flag value must be 0 (approved) or 1 (flagged)"
        }))
        the_response.status_code = 400
        return the_response

    # Update the flag
    update_query = '''
        UPDATE coopPositions
        SET flag = %s
        WHERE coopPositionId = %s
    '''

    cursor.execute(update_query, (value, pos_id))
    db.get_db().commit()

    flag_status = "flagged" if value == 1 else "approved"
    the_response = make_response(jsonify({
        "ok": True,
        "positionId": pos_id,
        "flag": value,
        "status": flag_status,
        "message": f"Position {pos_id} has been {flag_status}"
    }))
    the_response.status_code = 200
    return the_response

# Admin removes a flag from a position
@coopPositions.route('/coopPositions/<int:pos_id>/unflag', methods=['PUT'])
def unflag_position(pos_id):
    current_app.logger.info('PUT /coopPositions/%s/unflag route', pos_id)

    # First check if the position exists
    check_query = '''
        SELECT coopPositionId, flag
        FROM coopPositions
        WHERE coopPositionId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(check_query, (pos_id,))
    position = cursor.fetchone()

    if not position:
        the_response = make_response(jsonify({
            "ok": False,
            "error": f"Position {pos_id} not found"
        }))
        the_response.status_code = 404
        return the_response

    # Update the flag to FALSE (unflag)
    update_query = '''
        UPDATE coopPositions
        SET flag = FALSE
        WHERE coopPositionId = %s
    '''

    cursor.execute(update_query, (pos_id,))
    db.get_db().commit()

    the_response = make_response(jsonify({
        "ok": True,
        "positionId": pos_id,
        "flag": 0,
        "status": "approved",
        "message": f"Position {pos_id} has been unflagged (approved)"
    }))
    the_response.status_code = 200
    return the_response

@coopPositions.route('/allPositions', methods=['GET'])
def get_all_positions():
    current_app.logger.info('GET /allPositions route')
    query = '''
        SELECT
            coopPositionId,
            title,
            location,
            description,
            hourlyPay,
            desiredGPA,
            deadline,
            startDate,
            endDate,
            industry
        FROM coopPositions
        ORDER BY deadline ASC, coopPositionId DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Get next available co-op position ID (thread-safe)
@coopPositions.route('/coopPositions/nextId', methods=['GET'])
def get_next_position_id():
    current_app.logger.info('GET /coopPositions/nextId route')

    try:
        cursor = db.get_db().cursor()

        # Use a transaction to ensure thread safety
        cursor.execute('START TRANSACTION')

        # Get the maximum ID with a lock to prevent race conditions
        query = '''
            SELECT COALESCE(MAX(coopPositionId), 0) + 1 as nextId
            FROM coopPositions
            FOR UPDATE
        '''

        cursor.execute(query)
        result = cursor.fetchone()
        next_id = result['nextId']

        # Commit the transaction
        cursor.execute('COMMIT')

        current_app.logger.info(f'Next available position ID: {next_id}')

        the_response = make_response(jsonify({
            "nextId": next_id,
            "message": f"Next available position ID is {next_id}"
        }))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        # Rollback on error
        try:
            cursor.execute('ROLLBACK')
        except:
            pass
        current_app.logger.error(f"Error getting next position ID: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# Get positions created by a specific employer
@coopPositions.route('/employers/<int:employerId>/positions', methods=['GET'])
def get_employer_positions(employerId):
    current_app.logger.info('GET /employers/%s/positions', employerId)

    query = '''
        SELECT cp.coopPositionId, cp.title, cp.description, cp.location,
               cp.hourlyPay, cp.startDate, cp.endDate, cp.deadline,
               cp.industry, comp.name as companyName
        FROM coopPositions cp
        JOIN createsPos crp ON cp.coopPositionId = crp.coopPositionId
        LEFT JOIN users emp ON crp.employerId = emp.userId
        LEFT JOIN companyProfiles comp ON emp.companyProfileId = comp.companyProfileId
        WHERE crp.employerId = %s
        ORDER BY cp.deadline DESC;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (employerId,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

