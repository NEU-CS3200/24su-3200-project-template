from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

advisoradvisee = Blueprint('advisoradvisee', __name__)

# Advisor identifies students with too few applications
@advisoradvisee.route('/advisor/<advisorID>/students/low-applications', methods=['GET'])
def get_students_with_low_applications(advisorID):
    current_app.logger.info('GET /advisor/<advisorID>/students/low-applications route')

    query = '''
        SELECT u.userId,
               u.firstName,
               u.lastName,
               COUNT(apps.applicationId) AS totalApps
        FROM advisor_advisee aa
                JOIN users u ON u.userId = aa.studentId
                LEFT JOIN appliesToApp ata ON ata.studentId = u.userId
                LEFT JOIN applications apps ON ata.applicationId = apps.applicationId
        WHERE aa.advisorId = {0}
        GROUP BY u.userId, u.firstName, u.lastName
        HAVING COUNT(apps.applicationId) < 5
        ORDER BY totalApps ASC, u.lastName;
        '''.format(advisorID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Admin reassigns students to different advisors as needed
@advisoradvisee.route('/admin/<studentId>/<advisorId>', 
                      methods = ['PUT'])
def reassignAdvisor():
    current_app.logger.info('PUT /admin/<studentId>/<advisorId> route')
    advisorId = request.json
    studentId = request.json
    
    query = '''
    UPDATE advisor_advisee
            SET advisorId = %s
            WHERE studentId = %s;
            '''
    data=(advisorId, studentId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'advisor reassigned successfully'
    
