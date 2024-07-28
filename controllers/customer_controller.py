from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from init import db, ma
from models.customer import Customer, CustomerSchema

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# GET ALL CUSTOMERS
@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    stmt = db.select(Customer).order_by(Customer.fname)
    customers = db.session.scalars(stmt)
    return customers_schema.dump(customers), 200

# GET CUSTOMER VIA ID
@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        return customer_schema.dump(customer), 200
    else:
        return {"error": f"Customer with id {customer_id} not found"}, 404

# CREATE CUSTOMER
@customer_bp.route('/', methods=['POST'])
#@jwt_required()
def create_customer():
    # user_id = get_jwt_identity()
    # user = db.session.scalar(db.select(User).filter_by(id=user_id))
    # if user and user.role == 'employee':

    data = request.get_json()
    try:
        # Load data into schema to create a Customer instance
        customer_data = CustomerSchema().load(data)
        customer = Customer(**customer_data) # ** unpacks the dictionary
        db.session.add(customer)
        db.session.commit()
        return customer_schema.dump(customer), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE CUSTOMER
@customer_bp.route('/<int:customer_id>', methods=['PUT', 'PATCH'])
#@jwt_required()
def update_customer(customer_id):
    data = request.get_json()
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    print(data)
    if customer:
        try:
            customer_data = CustomerSchema(partial=True).load(data)
            for key, value in customer_data.items():
                setattr(customer, key, value)
            db.session.commit()
            return customer_schema.dump(customer), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Customer with id {customer_id} not found"}, 404 

# DELETE CUSTOMER
@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
#@jwt_required()
def delete_customer(customer_id):
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {"message": f"Customer '{customer_id}' deleted successfully"}, 200
    else:
        return {"error": f"Customer with id {customer_id} not found"}, 404
