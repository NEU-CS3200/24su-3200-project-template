from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

sections = Blueprint('sections', __name__)

# Get all sections for a professor
@sections.route('/<professor_id>/sections', methods=['GET'])
def get_sections_by_professor(professor_id):
    cursor = db.get_db().cursor()
    query = '''
    SELECT s.section_num, s.semester_year, c.course_name, d.deptName
    FROM Section s
    JOIN Class c on s.course_id = c.course_id
    JOIN Department d ON c.dept_id = d.dept_id
    WHERE s.professor_id = %s

    '''
    cursor.execute(query, (professor_id,))
    sections = cursor.fetchall()
    return jsonify(sections)

# !!!!! just added this - this one should work! 
# Get all students in prof's sections 
@sections.route('/<prof_id>/students', methods=['GET'])
def get_prof_students(prof_id):
    cursor = db.get_db().cursor()
    query = '''
    SELECT ss.student_id, first_name, last_name, email, ss.course_id, ss.semester_year, ss.section_num
    FROM StudentSection ss JOIN Student s ON ss.student_id = s.student_id
    WHERE ss.section_num IN (SELECT s.section_num
        FROM Section s
        WHERE s.professor_id = %s)
        AND ss.semester_year IN (SELECT s.semester_year
            FROM Section s
            WHERE s.professor_id = %s)
        AND ss.course_id IN (SELECT s.course_id
            FROM Section s
            WHERE s.professor_id = %s)
    '''
    cursor.execute(query, (prof_id, prof_id, prof_id))
    sections = cursor.fetchall()
    return jsonify(sections)

# Updated route for fetching students in a specific section
@sections.route('/sections/<int:section_num>/students', methods=['GET'])
def get_students_in_section(section_num):
    cursor = db.get_db().cursor()
    query = '''
        SELECT s.student_id, s.first_name, s.last_name, s.email
        FROM Student s
        JOIN StudentSection ss ON s.student_id = ss.student_id
        WHERE ss.section_num = %s
    '''
    cursor.execute(query, (section_num,))
    students = cursor.fetchall()
    return jsonify(students)


# Add a new section (for admin purposes)
@sections.route('/sections', methods=['POST'])
def add_section():
    section_data = request.json
    current_app.logger.info(section_data)

    section_num = section_data['section_num']
    semester_year = section_data['semester_year']
    course_id = section_data['course_id']
    professor_id = section_data.get('professor_id')

    query = '''
        INSERT INTO Section (section_num, semester_year, course_id, professor_id)
        VALUES (%s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (section_num, semester_year, course_id, professor_id))
    db.get_db().commit()
    
    return 'Section added successfully!', 201

# Update a section's information
@sections.route('/sections/<int:section_num>/<string:semester_year>', methods=['PUT'])
def update_section(section_num, semester_year):
    section_data = request.json
    current_app.logger.info(section_data)

    course_id = section_data.get('course_id')
    professor_id = section_data.get('professor_id')

    query = '''
        UPDATE Section 
        SET course_id = %s, professor_id = %s
        WHERE section_num = %s AND semester_year = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (course_id, professor_id, section_num, semester_year))
    db.get_db().commit()
    
    return 'Section updated successfully!', 200

