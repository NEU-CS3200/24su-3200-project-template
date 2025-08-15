from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import logging

logger = logging.getLogger(__name__)

users = Blueprint('users', __name__)

# Get student profiles with demographics
@users.route('/users/<userID>', methods=['GET'])
def get_user(userID):
    query = '''
        SELECT u.*, d.gender, d.race, d.nationality, d.sexuality, d.disability
        FROM users u
        LEFT JOIN demographics d ON u.userId = d.demographicId
        WHERE u.userId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (userID,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Get student skills with proficiency levels
@users.route('/users/<userID>/skills', methods=['GET'])
def get_user_skills(userID):
    current_app.logger.info(f'GET /users/{userID}/skills route')

    query = '''
        SELECT s.skillId, s.name, s.category, sd.proficiencyLevel
        FROM skills s
        JOIN skillDetails sd ON s.skillId = sd.skillId
        WHERE sd.studentId = %s
        ORDER BY s.category, s.name
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (userID,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Get recent applications for dashboard (limit 5)
@users.route('/users/<userID>/recent-applications', methods=['GET'])
def get_user_recent_applications(userID):
    current_app.logger.info(f'GET /users/{userID}/recent-applications route')

    query = '''
        SELECT a.applicationId,
               a.status,
               a.dateTimeApplied,
               a.gpa,
               cp.title AS positionTitle,
               cp.location,
               cp.hourlyPay,
               cp.deadline,
               com.name AS companyName
        FROM applications a
        JOIN appliesToApp ata ON a.applicationId = ata.applicationId
        JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
        JOIN createsPos crp ON cp.coopPositionId = crp.coopPositionId
        JOIN users emp ON crp.employerId = emp.userId
        JOIN companyProfiles com ON emp.companyProfileId = com.companyProfileId
        WHERE ata.studentId = %s
        ORDER BY a.dateTimeApplied DESC
        LIMIT 5
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (userID,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Get all available skills
@users.route('/skills', methods=['GET'])
def get_all_skills():
    query = '''
        SELECT skillId, name, category
        FROM skills
        ORDER BY category, name
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Update user skills (modify proficiency levels and remove skills)
@users.route('/users/<userID>/skills', methods=['PUT'])
def update_user_skills(userID):
    try:
        data = request.get_json()
        updated_skills = data.get('updated_skills', [])
        removed_skills = data.get('removed_skills', [])

        cursor = db.get_db().cursor()

        # Update existing skills proficiency levels
        for skill in updated_skills:
            update_query = '''
                UPDATE skillDetails
                SET proficiencyLevel = %s
                WHERE studentId = %s AND skillId = %s
            '''
            cursor.execute(update_query, (skill['proficiencyLevel'], userID, skill['skillId']))

        # Remove skills marked for deletion
        if removed_skills:
            placeholders = ','.join(['%s'] * len(removed_skills))
            delete_query = f'''
                DELETE FROM skillDetails
                WHERE studentId = %s AND skillId IN ({placeholders})
            '''
            cursor.execute(delete_query, [userID] + removed_skills)

        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Skills updated successfully"}))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        logger.error(f"Error updating user skills: {e}")
        the_response = make_response(jsonify({"error": "Failed to update skills"}))
        the_response.status_code = 500
        return the_response

# Add new skills to user profile
@users.route('/users/<userID>/skills', methods=['POST'])
def add_user_skills(userID):
    try:
        data = request.get_json()
        new_skills = data.get('skills', [])

        if not new_skills:
            the_response = make_response(jsonify({"error": "No skills provided"}))
            the_response.status_code = 400
            return the_response

        cursor = db.get_db().cursor()

        # Add new skills to skillDetails table
        for skill in new_skills:
            insert_query = '''
                INSERT INTO skillDetails (skillId, studentId, proficiencyLevel)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(insert_query, (skill['skillId'], userID, skill['proficiencyLevel']))

        db.get_db().commit()

        the_response = make_response(jsonify({"message": f"Added {len(new_skills)} skills successfully"}))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        logger.error(f"Error adding user skills: {e}")
        the_response = make_response(jsonify({"error": "Failed to add skills"}))
        the_response.status_code = 500
        return the_response

# Get advisor's assigned students
@users.route('/advisors/<advisorID>/students', methods=['GET'])
def get_advisor_students(advisorID):
    query = '''
        SELECT u.userId, u.firstName, u.lastName, u.email, u.phone,
               u.major, u.minor, u.college, u.gradYear, u.grade,
               d.gender, d.race, d.nationality, d.sexuality, d.disability,
               aa.flag as flagged
        FROM users u
        LEFT JOIN demographics d ON u.userId = d.demographicId
        JOIN advisor_advisee aa ON u.userId = aa.studentId
        WHERE aa.advisorId = %s
        ORDER BY u.lastName, u.firstName
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (advisorID,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Update student flag status for advisor
@users.route('/advisors/<advisorID>/students/<studentID>/flag', methods=['PUT'])
def update_student_flag(advisorID, studentID):
    try:
        data = request.get_json()
        flagged = data.get('flagged', False)

        query = '''
            UPDATE advisor_advisee
            SET flag = %s
            WHERE advisorId = %s AND studentId = %s
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (flagged, advisorID, studentID))
        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Student flag updated successfully", "flagged": flagged}))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        logger.error(f"Error updating student flag: {e}")
        the_response = make_response(jsonify({"error": "Failed to update student flag"}))
        the_response.status_code = 500
        return the_response

# Get placement analytics data for advisor
@users.route('/advisors/<advisorID>/analytics/placement-data', methods=['GET'])
def get_advisor_placement_analytics(advisorID):
    try:
        query = '''
            SELECT
                u.firstName,
                u.lastName,
                u.gradYear,
                u.major,
                u.college,
                a.gpa,
                a.status,
                cp.title as positionTitle,
                cp.hourlyPay as salary,
                comp.name as companyName,
                cp.industry
            FROM users u
            JOIN advisor_advisee aa ON u.userId = aa.studentId
            JOIN appliesToApp ata ON u.userId = ata.studentId
            JOIN applications a ON ata.applicationId = a.applicationId
            JOIN coopPositions cp ON a.coopPositionId = cp.coopPositionId
            LEFT JOIN createsPos crp ON cp.coopPositionId = crp.coopPositionId
            LEFT JOIN users emp ON crp.employerId = emp.userId
            LEFT JOIN companyProfiles comp ON emp.companyProfileId = comp.companyProfileId
            WHERE aa.advisorId = %s
                AND a.status IN ('Accepted', 'Rejected')
                AND cp.hourlyPay IS NOT NULL
                AND a.gpa IS NOT NULL

            UNION ALL

            SELECT
                u.firstName,
                u.lastName,
                u.gradYear,
                u.major,
                u.college,
                avg_gpa.gpa as gpa,
                'Completed' as status,
                cp.title as positionTitle,
                cp.hourlyPay as salary,
                comp.name as companyName,
                cp.industry
            FROM users u
            JOIN advisor_advisee aa ON u.userId = aa.studentId
            JOIN workedAtPos wap ON u.userId = wap.studentId
            JOIN coopPositions cp ON wap.coopPositionId = cp.coopPositionId
            LEFT JOIN createsPos crp ON cp.coopPositionId = crp.coopPositionId
            LEFT JOIN users emp ON crp.employerId = emp.userId
            LEFT JOIN companyProfiles comp ON emp.companyProfileId = comp.companyProfileId
            LEFT JOIN (
                SELECT ata.studentId, AVG(a.gpa) as gpa
                FROM appliesToApp ata
                JOIN applications a ON ata.applicationId = a.applicationId
                WHERE a.gpa IS NOT NULL
                GROUP BY ata.studentId
            ) avg_gpa ON u.userId = avg_gpa.studentId
            WHERE aa.advisorId = %s
                AND cp.hourlyPay IS NOT NULL

            ORDER BY lastName, firstName
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (advisorID, advisorID))
        theData = cursor.fetchall()

        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        logger.error(f"Error fetching placement analytics: {e}")
        the_response = make_response(jsonify({"error": "Failed to fetch placement analytics"}))
        the_response.status_code = 500
        return the_response



# Update advisor profile (separate from student profile updates)
@users.route('/advisors/<advisorID>/profile', methods=['PUT'])
def update_advisor_profile(advisorID):
    try:
        current_app.logger.info(f'PUT /advisors/{advisorID}/profile route')
        advisor_info = request.json

        first_name = advisor_info.get('firstName')
        last_name = advisor_info.get('lastName')
        email = advisor_info.get('email')
        phone = advisor_info.get('phone')
        gender = advisor_info.get('gender')
        race = advisor_info.get('race')
        nationality = advisor_info.get('nationality')
        sexuality = advisor_info.get('sexuality')
        disability = advisor_info.get('disability')

        # Update users table (basic info)
        user_query = '''
            UPDATE users
            SET firstName = %s,
                lastName = %s,
                email = %s,
                phone = %s
            WHERE userId = %s
        '''

        # Update demographics table
        demo_query = '''
            UPDATE demographics
            SET gender = %s,
                race = %s,
                nationality = %s,
                sexuality = %s,
                disability = %s
            WHERE demographicId = %s
        '''

        cursor = db.get_db().cursor()

        # Execute user update
        cursor.execute(user_query, (first_name, last_name, email, phone, advisorID))

        # Execute demographics update
        cursor.execute(demo_query, (gender, race, nationality, sexuality, disability, advisorID))

        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Advisor profile updated successfully"}))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        logger.error(f"Error updating advisor profile: {e}")
        the_response = make_response(jsonify({"error": "Failed to update advisor profile"}))
        the_response.status_code = 500
        return the_response

# Update student profiles to include additional info
@users.route('/users', methods=['PUT'])
def update_users():
    current_app.logger.info('PUT /users route')
    user_info = request.json
    user_id = user_info['userId']
    first_name = user_info['firstName']
    last_name = user_info['lastName']
    email = user_info['email']
    phone = user_info['phone']
    major = user_info['major']
    minor = user_info['minor']
    college = user_info['college']
    grad_year = user_info['gradYear']
    grade = user_info['grade']
    gender = user_info['gender']
    race = user_info['race']
    nationality = user_info['nationality']
    sexuality = user_info['sexuality']
    disability = user_info['disability']

    query = '''
        UPDATE users u
        JOIN demographics d ON u.userId = d.demographicId
        SET u.firstName = %s,
            u.lastName = %s,
            u.email = %s,
            u.phone = %s,
            u.major = %s,
            u.minor = %s,
            u.college = %s,
            u.gradYear = %s,
            u.grade = %s,
            d.gender = %s,
            d.race = %s,
            d.nationality = %s,
            d.sexuality = %s,
            d.disability = %s
        WHERE u.userId = %s;'''
    data = (first_name, last_name, email, phone, major, minor, college, grad_year, grade, gender, race, nationality, sexuality, disability, user_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'user updated!'


# Employer views student profile
@users.route('/applications/appliesToApp/<studentId>/users', methods=['GET'])
def employer_view_student():
    current_app.logger.info('GET /applications/appliesToApp/<studentId>/users')
    user_info = request.json
    application_info = request.json
    user_id = user_info['userId']
    first_name = user_info['firstName']
    last_name = user_info['lastName']
    email = user_info['email']
    major = user_info['major']
    minor = user_info['minor']
    college = user_info['college']
    grade = user_info['grade']
    grad_year = user_info['gradYear']
    gpa = application_info['gpa']
    resume = application_info['resume']
    cover_letter = application_info['coverLetter']


    query = '''
        SELECT u.userId, u.firstName, u.lastName, u.email, u.major,
       u.minor, u.college, u.grade, u.gradYear, a.gpa,
       a.resume, a.coverLetter
       FROM users u JOIN applications a;'''
    data = (first_name, last_name, email, major, minor, college, grad_year, grade, user_id,
            gpa, resume, cover_letter)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()


    theData = cursor.fetchall()
   
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Employer filters student profiles
@users.route('/applications/appliesToApp/<studentId>/users', methods=['GET'])
def employee_filter_student():
    current_app.logger.info('GET /applications/appliesToApp/<studentId>/users')
    user_info = request.json
    skill_info = request.json
    user_id = user_info['userId']
    first_name = user_info['firstName']
    last_name = user_info['lastName']
    name = skill_info['name']
    grad_year = user_info['gradYear']
    major = user_info['major']

    query = '''
        SELECT DISTINCT u.userId, u.firstName, u.lastName, u.gradYear, u.major
        FROM users u
        JOIN skillDetails sd ON u.userId = sd.studentId
        JOIN skills s ON sd.skillId = s.skillId
        WHERE (s.name = %s OR s.name = %s OR s.name = %s)
          AND u.gradYear = %s
          AND u.major = %s;
    '''
    data = (skill1, skill2, skill3, grad_year, major)

    cursor = db.get_db().cursor(dictionary=True)
    cursor.execute(query, data)
    theData = cursor.fetchall()

    return make_response(jsonify(theData), 200)

# Admin creates a user (student/employer/advisor)
@users.route('/users', methods=['POST'])
def create_user():
    current_app.logger.info('POST /users route')

    b = request.json
    user_id = b['userId']
    first_name = b['firstName']
    last_name = b['lastName']
    email = b['email']
    phone = b.get('phone')
    major = b.get('major')
    minor = b.get('minor')
    college = b.get('college')
    grad_year = b.get('gradYear')
    grade = b.get('grade')
    company_profile_id = b.get('companyProfileId')   
    industry = b.get('industry')
    demographic_id = b.get('demographicId')        

    query = '''
        INSERT INTO users
            (userId, firstName, lastName, demographicId, email, phone,
             major, minor, college, gradYear, grade, companyProfileId, industry)
        VALUES
            (%s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s, %s);
    '''
    data = (user_id, first_name, last_name, demographic_id, email, phone,major, minor, college, grad_year, grade, company_profile_id, industry)

    cur = db.get_db().cursor()
    cur.execute(query, data)
    db.get_db().commit()
    return 'user created!', 201

# Admin deletes a user
@users.route('/users', methods=['DELETE'])
def delete_user():
    current_app.logger.info('DELETE /users route')

    user_id = request.args.get('userId', type=int)

    query = '''
        DELETE FROM users
        WHERE userId = %s;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    db.get_db().commit()

    the_response = make_response(jsonify({'message': 'user deleted!'}))

    the_response.status_code = 200
    return the_response

# Employer creates a company profile
@users.route('/users/companyProfiles/create', methods=['POST'])
def createCompanyProfile():
    
    the_data = request.json
    current_app.logger.info(the_data)
    
    name = the_data['company_name']
    bio = the_data['company_bio']
    industry = the_data['company_industry']
    websiteLink = the_data['website_link']
        
    query = f'''
    INSERT INTO companyProfiles (name, bio, industry, websiteLink)
    VALUE( '{name}', '{bio}', '{industry}', '{websiteLink}')
    '''
    
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Created company profile")
    response.status_code = 200
    return response

# Employer updates/edits company information
@users.route('/users/companyProfiles/create/<companyProfileId>', methods=['PUT'])
def updateCompanyProfile(companyProfileId):
    current_app.logger.info('PUT /users/companyProfiles/create/<companyProfileId> route')
    
    company_info = request.json
    companyId = company_info['id']
    companyName = company_info['name']
    companyBio = company_info['bio']
    companyIndustry = company_info['industry']
    companyWebsite = company_info['website_link']
    
    query = '''
        UPDATE companyProfiles
        SET name = %s,
            bio = %s,
            industry = %s,
            websiteLink = %s
        WHERE companyProfileId = %s
    '''
    data = (companyName, companyBio, companyIndustry, companyWebsite, companyId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Updated company profile!'

# Get count of students
@users.route('/users/count/students', methods=['GET'])
def count_students():
    current_app.logger.info('GET /users/count/students route')
    
    try:
        query = '''
            SELECT COUNT(*) as student_count
            FROM users
            WHERE major IS NOT NULL AND major != '' AND companyProfileId IS NULL;
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        the_response = make_response(jsonify({"student_count": result['student_count']}))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error counting students: {e}")
        logger.error(f"Error counting students: {e}")
        the_response = make_response(jsonify({"error": f"Failed to count students: {str(e)}"}))
        the_response.status_code = 500
        return the_response

# Get count of advisors
@users.route('/users/count/advisors', methods=['GET'])
def count_advisors():
    current_app.logger.info('GET /users/count/advisors route')
    
    try:
        query = '''
            SELECT COUNT(DISTINCT aa.advisorId) as advisor_count
            FROM advisor_advisee aa;
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        the_response = make_response(jsonify({"advisor_count": result['advisor_count']}))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error counting advisors: {e}")
        logger.error(f"Error counting advisors: {e}")
        the_response = make_response(jsonify({"error": f"Failed to count advisors: {str(e)}"}))
        the_response.status_code = 500
        return the_response

# Get count of employers
@users.route('/users/count/employers', methods=['GET'])
def count_employers():
    current_app.logger.info('GET /users/count/employers route')
    
    try:
        query = '''
            SELECT COUNT(*) as employer_count
            FROM users
            WHERE companyProfileId IS NOT NULL;
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        the_response = make_response(jsonify({"employer_count": result['employer_count']}))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error counting employers: {e}")
        logger.error(f"Error counting employers: {e}")
        the_response = make_response(jsonify({"error": f"Failed to count employers: {str(e)}"}))
        the_response.status_code = 500
        return the_response

# Get all user counts in one request
@users.route('/users/count/all', methods=['GET'])
def count_all_users():
    current_app.logger.info('GET /users/count/all route')
    
    try:
        # Count students
        student_query = '''
            SELECT COUNT(*) as student_count
            FROM users
            WHERE major IS NOT NULL AND major != '' AND companyProfileId IS NULL
        '''
        
        # Count advisors
        advisor_query = '''
            SELECT COUNT(DISTINCT aa.advisorId) as advisor_count
            FROM advisor_advisee aa
        '''
        
        # Count employers
        employer_query = '''
            SELECT COUNT(*) as employer_count
            FROM users
            WHERE companyProfileId IS NOT NULL
        '''
        
        cursor = db.get_db().cursor()
        
        # Execute all queries
        cursor.execute(student_query)
        student_count = cursor.fetchone()['student_count']
        
        cursor.execute(advisor_query)
        advisor_count = cursor.fetchone()['advisor_count']
        
        cursor.execute(employer_query)
        employer_count = cursor.fetchone()['employer_count']
        
        counts = {
            "student_count": student_count,
            "advisor_count": advisor_count,
            "employer_count": employer_count,
            "total_users": student_count + advisor_count + employer_count
        }
        
        the_response = make_response(jsonify(counts))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error counting all users: {e}")
        logger.error(f"Error counting all users: {e}")
        the_response = make_response(jsonify({"error": f"Failed to count users: {str(e)}"}))
        the_response.status_code = 500
        return the_response