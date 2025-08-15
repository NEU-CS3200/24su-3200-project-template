from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

workedatpos = Blueprint('workedatpos', __name__)

# Advisor views historical placement data for all students (filter by major/industry in frontend)
@workedatpos.route('/workedatpos/placement-data', methods=['GET'])
def get_scatter_plot_data():
    current_app.logger.info('GET /workedatpos/placement-data route')
    
    query = '''
        SELECT u.major,
               cp.industry,
               a.gpa,
               cp.hourlyPay,
               wp.studentId AS wasHired,
               u.firstName,
               u.lastName,
               cp.title AS positionTitle,
               comp.name AS companyName,
               u.college,
               u.gradYear,
               cp.location
        FROM users u
                 JOIN appliesToApp ata ON u.userId = ata.studentId
                 JOIN applications a ON ata.applicationId = a.applicationId
                 JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
                 JOIN companyProfiles comp ON cp.industry = comp.industry
                 LEFT JOIN workedAtPos wp ON u.userId = wp.studentId AND wp.coopPositionId = cp.coopPositionId
        WHERE a.gpa IS NOT NULL 
          AND cp.hourlyPay IS NOT NULL
        ORDER BY u.major, cp.industry, a.gpa DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.headers.add('Access-Control-Allow-Origin', '*')
    the_response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return the_response

# Advisor and student views company rating data rated by past co-ops
@workedatpos.route('/workedatpos/company-ratings', methods=['GET'])
def get_company_ratings():
    current_app.logger.info('GET /workedatpos/company-ratings route')
    
    # Query to get company ratings by individual company
    query = '''
        SELECT 
            comp.companyProfileId,
            comp.name AS companyName,
            comp.industry AS companyIndustry,
            AVG(wp.companyRating) AS avgRating,
            COUNT(wp.companyRating) AS totalRatings,
            MIN(wp.companyRating) AS minRating,
            MAX(wp.companyRating) AS maxRating,
            COUNT(DISTINCT wp.studentId) AS studentsWhoRated
        FROM workedAtPos wp
        JOIN coopPositions cp ON wp.coopPositionId = cp.coopPositionId
        JOIN companyProfiles comp ON cp.industry = comp.industry
        WHERE wp.companyRating IS NOT NULL
        GROUP BY comp.companyProfileId, comp.name, comp.industry
        ORDER BY avgRating DESC;
        '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.headers.add('Access-Control-Allow-Origin', '*')
    the_response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return the_response

# Student views wage data from past co-ops
@workedatpos.route('/workedatpos/wagedata', methods=['GET'])
def get_company_wage_data():
    current_app.logger.info('GET /workedatpos/wagedata route')

    query = '''
        SELECT cp.name AS companyName,
               pos.title AS positionTitle,
                MIN(pos.hourlyPay) AS minSalary,
                MAX(pos.hourlyPay) AS maxSalary,
                AVG(pos.hourlyPay) AS avgPay,
                COUNT(w.studentId) AS numPreviousCoops
        FROM companyProfiles cp JOIN users u ON cp.companyProfileId = u.companyProfileId
            JOIN createsPos cr ON u.userId = cr.employerId
            JOIN coopPositions pos ON cr.coopPositionId = pos.coopPositionId
            LEFT JOIN workedAtPos w ON pos.coopPositionId = w.coopPositionId
        GROUP BY cp.name, pos.title
        ORDER BY avgPay DESC;

        '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.headers.add('Access-Control-Allow-Origin', '*')
    the_response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return the_response

