from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, ma
from models.theater import Theater, TheaterSchema


theater_bp = Blueprint('theater', __name__, url_prefix='/theaters')

theater_schema = TheaterSchema()
theaters_schema = TheaterSchema(many=True)

# GET ALL THEATERS
@theater_bp.route('/', methods=['GET'])
def get_all_theaters():
    stmt = db.select(Theater).order_by(Theater.name)
    theaters = db.session.scalars(stmt)
    return theaters_schema.dump(theaters), 200

# GET THEATER VIA ID
@theater_bp.route('/<int:theater_id>', methods=['GET'])
def get_theater(theater_id):
    stmt = db.select(Theater).filter_by(id=theater_id)
    theater = db.session.scalar(stmt)
    if theater:
        return theater_schema.dump(theater), 200
    else:
        return {"error": f"Theater with id {theater_id} not found"}, 404

# CREATE THEATER
@theater_bp.route('/', methods=['POST'])
#@jwt_required()
def create_theater():
    # user_id = get_jwt_identity()
    # user = db.session.scalar(db.select(User).filter_by(id=user_id))
    # if user and user.role == 'employee':

    data = request.get_json()
    try:
        # Load data into schema to create a Theater instance
        theater_data = TheaterSchema().load(data)
        theater = Theater(**theater_data) # ** unpacks the dictionary
        db.session.add(theater)
        db.session.commit()
        return theater_schema.dump(theater), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE THEATER
@theater_bp.route('/<int:theater_id>', methods=['PUT', 'PATCH'])
#@jwt_required()
def update_theater(theater_id):
    data = request.get_json()
    stmt = db.select(Theater).filter_by(id=theater_id)
    theater = db.session.scalar(stmt)
    print(data)
    if theater:
        try:
            theater_data = TheaterSchema(partial=True).load(data)
            for key, value in theater_data.items():
                setattr(theater, key, value)
            db.session.commit()
            return theater_schema.dump(theater), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Theater with id {theater_id} not found"}, 404 

# DELETE THEATER
@theater_bp.route('/<int:theater_id>', methods=['DELETE'])
#@jwt_required()
def delete_theater(theater_id):
    stmt = db.select(Theater).filter_by(id=theater_id)
    theater = db.session.scalar(stmt)
    if theater:
        db.session.delete(theater)
        db.session.commit()
        return {"message": f"Theater '{theater_id}' deleted successfully"}, 200
    else:
        return {"error": f"Theater with id {theater_id} not found"}, 404
