from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from init import db, ma, bcrypt
from models.employee import Employee, EmployeeSchema
from decorator import role_check

employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# GET ALL EMPLOYEES
@employee_bp.route('/', methods=['GET'])
@role_check('Manager')
def get_all_employees():
    stmt = db.select(Employee).order_by(Employee.fname)
    employees = db.session.scalars(stmt)
    return employees_schema.dump(employees), 200

# GET EMPLOYEE VIA ID
@employee_bp.route('/<int:employee_id>', methods=['GET'])
@role_check('Manager')
def get_employee(employee_id):
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    if employee:
        return employee_schema.dump(employee), 200
    else:
        return {"error": f"Employee with id {employee_id} not found"}, 404

# CREATE EMPLOYEE
@employee_bp.route('/', methods=['POST'])
@role_check('Manager')
def create_employee():
    data = request.get_json()
    try:
        # Load data into schema to create a Employee instance
        employee_data = EmployeeSchema().load(data)
        employee_data['password'] = bcrypt.generate_password_hash(employee_data['password']).decode('utf-8')
        employee = Employee(**employee_data) # ** unpacks the dictionary
        db.session.add(employee)
        db.session.commit()
        return employee_schema.dump(employee), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE EMPLOYEE
@employee_bp.route('/<int:employee_id>', methods=['PUT', 'PATCH'])
@role_check('Manager')
def update_employee(employee_id):
    data = request.get_json()
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    print(data)
    if employee:
        try:
            employee_data = EmployeeSchema(partial=True).load(data)
            for key, value in employee_data.items():
                setattr(employee, key, value)
            db.session.commit()
            return employee_schema.dump(employee), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Employee with id {employee_id} not found"}, 404 

# DELETE EMPLOYEE
@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
#@jwt_required()
def delete_employee(employee_id):
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {"message": f"Employee '{employee_id}' deleted successfully"}, 200
    else:
        return {"error": f"Employee with id {employee_id} not found"}, 404
