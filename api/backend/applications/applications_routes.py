from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import pymysql

# New Blueprint for applications
applications = Blueprint('applications', __name__)


# Student viewing their own application statuses
@applications.route('/student/<studentID>/applications', methods=['GET'])
def get_student_applications(studentID):
    current_app.logger.info(f'GET /student/{studentID}/applications route')
    
    query = '''
        SELECT u.userId,
               u.firstName,
               u.lastName,
               a.applicationId,
               a.status AS applicationStatus,
               a.resume,
               a.coverLetter,
               a.gpa,
               cp.title AS positionTitle,
               cp.deadline AS applicationDeadline,
               a.dateTimeApplied,
               cp.description AS positionDescription
        FROM users u
        JOIN appliesToApp ata ON u.userId = ata.studentId
        JOIN applications a ON ata.applicationId = a.applicationId
        JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
        WHERE u.userId = %s
        ORDER BY a.dateTimeApplied DESC, cp.deadline ASC
    '''

    connection = db.get_db()

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, (studentID,))
    theData = cursor.fetchall()
    
    return make_response(jsonify(theData), 200)

# student sees how many positions they have applied to
@applications.route('/student/<studentID>/applications/summary', methods=['GET'])
def get_numb_apps(studentID):
    current_app.logger.info('GET /student/<studentID>/applications route')
    
    query = '''
        SELECT a.status, 
            COUNT(*) AS ApplicationCount
        FROM applications a
            JOIN appliesToApp ata ON a.applicationId = ata.applicationId
        WHERE ata.studentId = %s
        GROUP BY a.status

    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (studentID,))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response



# Advisor viewing all their advisees' application statuses
@applications.route('/advisor/<advisorID>/students/applications', methods=['GET'])
def get_advisor_student_applications(advisorID):
    current_app.logger.info('GET /advisor/<advisorID>/students/applications route')
    
    query = '''
        SELECT aa.advisorId,
               u.userId,
               u.firstName,
               u.lastName,
               a.applicationId,
               a.status    AS applicationStatus,
               cp.title    AS positionTitle,
               cp.deadline AS applicationDeadline,
               com.name    AS companyName,
               a.dateApplied
        FROM advisor_advisee aa
                 JOIN users u ON aa.studentId = u.userId
                 JOIN appliesToApp ata ON u.userId = ata.studentId
                 JOIN applications a ON ata.applicationId = a.applicationId
                 JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
                 JOIN companyProfiles com ON cp.companyProfileId = com.companyProfileId
                 LEFT JOIN workedAtPos wp ON u.userId = wp.studentId AND wp.coopPositionId = cp.coopPositionId
        WHERE aa.advisorId = {0}
        ORDER BY u.lastName, u.firstName, a.dateApplied DESC
    '''.format(advisorID)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Employer views all applications of a posting
@applications.route('/applications/<int:coopPositionId>', methods=['GET'])
def get_applications(coopPositionId):
    current_app.logger.info('GET /applications/%s', coopPositionId)

    query = '''
        SELECT a.dateTimeApplied, a.status, a.resume, a.gpa, a.coverLetter,
               a.coopPositionId, a.applicationId
        FROM applications a
        JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
        WHERE a.coopPositionId = %s
        ORDER BY a.dateTimeApplied DESC;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (coopPositionId,))
    theData = cursor.fetchall()

    return make_response(jsonify(theData), 200)

# Employer views all applications with student details for a specific position
@applications.route('/applications/<int:coopPositionId>/with-students', methods=['GET'])
def get_applications_with_students(coopPositionId):
    current_app.logger.info('GET /applications/%s/with-students', coopPositionId)

    query = '''
        SELECT a.dateTimeApplied, a.status, a.resume, a.gpa, a.coverLetter,
               a.coopPositionId, a.applicationId,
               u.userId as studentId, u.firstName, u.lastName, u.email,
               u.major, u.minor, u.college, u.gradYear, u.grade
        FROM applications a
        JOIN appliesToApp ata ON a.applicationId = ata.applicationId
        JOIN users u ON ata.studentId = u.userId
        JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
        WHERE a.coopPositionId = %s
        ORDER BY a.dateTimeApplied DESC;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (coopPositionId,))
    theData = cursor.fetchall()

    return make_response(jsonify(theData), 200)

# Update application status (for employers)
@applications.route('/applications/<int:applicationId>/status', methods=['PUT'])
def update_application_status(applicationId):
    current_app.logger.info('PUT /applications/%s/status', applicationId)

    try:
        request_data = request.json
        new_status = request_data.get('status')

        if not new_status:
            return make_response(jsonify({"error": "Status is required"}), 400)

        # Validate status values
        valid_statuses = ['Draft', 'Submitted', 'Under Review', 'Accepted', 'Rejected']
        if new_status not in valid_statuses:
            return make_response(jsonify({"error": "Invalid status"}), 400)

        query = '''
            UPDATE applications
            SET status = %s
            WHERE applicationId = %s
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (new_status, applicationId))

        if cursor.rowcount == 0:
            return make_response(jsonify({"error": "Application not found"}), 404)

        db.get_db().commit()

        return make_response(jsonify({
            "success": True,
            "applicationId": applicationId,
            "newStatus": new_status
        }), 200)

    except Exception as e:
        current_app.logger.error(f"Error updating application status: {e}")
        return make_response(jsonify({"error": "Internal server error"}), 500)

# Get single application details by application ID
@applications.route('/applications/<int:applicationId>/details', methods=['GET'])
def get_application_details(applicationId):
    current_app.logger.info('GET /applications/%s/details', applicationId)

    query = '''
        SELECT a.applicationId, a.dateTimeApplied, a.status, a.resume, a.gpa, a.coverLetter,
               a.coopPositionId, cp.title as positionTitle, cp.location, cp.hourlyPay,
               cp.deadline, cp.industry, cp.description as positionDescription,
               u.userId as studentId, u.firstName, u.lastName, u.email,
               u.major, u.minor, u.college, u.gradYear, u.grade
        FROM applications a
        JOIN appliesToApp ata ON a.applicationId = ata.applicationId
        JOIN users u ON ata.studentId = u.userId
        JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
        WHERE a.applicationId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (applicationId,))
    theData = cursor.fetchall()

    if not theData:
        return make_response(jsonify({"error": "Application not found"}), 404)

    return make_response(jsonify(theData[0]), 200)

# Student applies to a position
@applications.route('/applications/new', methods=['POST'])
def create_application():
    current_app.logger.info('POST /applications/new')

    data = request.json
    required_fields = ['coopPositionId', 'studentId']

    if not all(field in data for field in required_fields):
        current_app.logger.warning('POST /applications/new missing required fields')
        return make_response(jsonify({"error": "coopPositionId and studentId are required"}), 400)

    try:
        cursor = db.get_db().cursor()

        # Insert application
        cursor.execute('''
            INSERT INTO applications (resume, gpa, coverLetter, coopPositionId)
            VALUES (%s, %s, %s, %s)
        ''', (
            data.get('resume', ''),
            data.get('gpa'),
            data.get('coverLetter', ''),
            data['coopPositionId']
        ))

        application_id = cursor.lastrowid

        # Link student to application
        cursor.execute('''
            INSERT INTO appliesToApp (applicationId, studentId)
            VALUES (%s, %s)
        ''', (application_id, data['studentId']))

        db.get_db().commit()
        return jsonify({"message": "Application submitted", "applicationId": application_id}), 201

    except Exception as e:
        current_app.logger.error(f"❌ Error creating application: {e}")
        return jsonify({"error": str(e)}), 500  # Temporarily return full error for debugging