from flask import Blueprint, request, jsonify
from init import bcrypt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.employee import Employee, EmployeeSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# IS THIS NECESSARY? CREATING A NEW EMPLOYEE ALREADY EXISTS
# @auth_bp.route('/register', methods=['POST'])

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if the employee exists and the password is correct
    employee = db.session.scalar(db.select(Employee).filter_by(email=data.get('email')))
    print(employee)

    if employee and bcrypt.check_password_hash(employee.password, data.get('password')):
        token = create_access_token(identity=employee.id)
        return ({'token': token, 'employee': EmployeeSchema().dump(employee)})
    return ({'error': 'Invalid email or password'}), 401

