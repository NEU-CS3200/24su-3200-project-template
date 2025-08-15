from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

demographics = Blueprint('demographics', __name__)

# DEI by employer 
@demographics.route('/demographics/employers/gender', methods=['GET'])
def dei_employers_gender():
    current_app.logger.info('GET /demographics/employers/gender route')
    query = '''
        SELECT
            com.name AS companyName,
            d.gender,
            COUNT(*) AS applicationCount
        FROM applications a
        JOIN appliesToApp ata ON ata.applicationId = a.applicationId
        JOIN users us         ON us.userId = ata.studentId              
        LEFT JOIN demographics d ON d.demographicId = us.userId
        JOIN coopPositions cp  ON cp.coopPositionId = a.coopPositionId
        JOIN createsPos cr     ON cr.coopPositionId = cp.coopPositionId
        JOIN users ue          ON ue.userId = cr.employerId           
        JOIN companyProfiles com ON com.companyProfileId = ue.companyProfileId
        GROUP BY com.name, d.gender
        ORDER BY com.name, d.gender;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    resp = make_response(jsonify(theData)); resp.status_code = 200
    return resp

# DEI by posting 
@demographics.route('/demographics/positions/gender', methods=['GET'])
def dei_positions_gender():
    current_app.logger.info('GET /demographics/positions/gender route')
    query = '''
        SELECT
            cp.coopPositionId,
            cp.title,
            com.name AS companyName,
            d.gender,
            COUNT(*) AS applicationCount
        FROM applications a
        JOIN appliesToApp ata ON ata.applicationId = a.applicationId
        JOIN users us         ON us.userId = ata.studentId             
        LEFT JOIN demographics d ON d.demographicId = us.userId
        JOIN coopPositions cp  ON cp.coopPositionId = a.coopPositionId
        JOIN createsPos cr     ON cr.coopPositionId = cp.coopPositionId
        JOIN users ue          ON ue.userId = cr.employerId            
        JOIN companyProfiles com ON com.companyProfileId = ue.companyProfileId
        GROUP BY cp.coopPositionId, cp.title, com.name, d.gender
        ORDER BY cp.title, d.gender;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    resp = make_response(jsonify(theData)); resp.status_code = 200
    return resp

# /api/dei/metrics 
@demographics.route('/api/dei/metrics', methods=['GET'])
def dei_metrics():
    current_app.logger.info('GET /api/dei/metrics route')
    query = '''
        SELECT 'gender'     AS metric, gender     AS label, COUNT(*) AS count
        FROM demographics
        WHERE gender IS NOT NULL
        GROUP BY gender

        UNION ALL
        SELECT 'race'       AS metric, race       AS label, COUNT(*) AS count
        FROM demographics
        WHERE race IS NOT NULL
        GROUP BY race

        UNION ALL
        SELECT 'nationality' AS metric, nationality AS label, COUNT(*) AS count
        FROM demographics
        WHERE nationality IS NOT NULL
        GROUP BY nationality

        UNION ALL
        SELECT 'disability' AS metric, disability AS label, COUNT(*) AS count
        FROM demographics
        WHERE disability IS NOT NULL
        GROUP BY disability

        ORDER BY metric, count DESC, label;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    resp = make_response(jsonify(theData)); resp.status_code = 200
    return resp