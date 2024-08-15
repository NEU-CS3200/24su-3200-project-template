from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

employees = Blueprint('employee', __name__)

# Gets employees id, email and username 
@employees.route('/employee', methods =['GET'])
def get_employees():
    cursor = db.get_db().cursor()
    cursor.execute('select id, email from employee')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Updates the employees personal information 
@employees.route ('/update_employee', methods = ['PUT'])
def update_employee():
    empl_info = request.json
    empl_id = empl_info['id']
    first = empl_info['first_name']
    last = empl_info['last_name']
    email = empl_info['email']

    query = 'UPDATE employee SET first_name = %s, last_name %s, email = %s where id = %s'
    data = (first, last, email, empl_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Employee Updated '

# Adding a new employee 
@employees.route('/add_employee', methods=['POST'])
def add_new_employee():
    the_data = request.json
    current_app.logger.info(the_data)
    first = the_data['first_name']
    last = the_data['last_name']
    id = the_data['id']
    email = the_data['email']
    

    query = 'insert into employee (first_name, last_name, id, email, user) values("'
    query += first + '", "'
    query += last + '", "'
    query += id + '", "' 
    query += email + ')'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db.commit()
    return 'Success'

