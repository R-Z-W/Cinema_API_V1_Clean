from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from init import db, ma
from models.showtime import Showtime, ShowtimeSchema
from decorator import role_check

showtime_bp = Blueprint('showtime', __name__, url_prefix='/showtimes')

showtime_schema = ShowtimeSchema()
showtimes_schema = ShowtimeSchema(many=True)

# GET ALL SHOWTIMES
@showtime_bp.route('/', methods=['GET'])
def get_all_showtimes():
    stmt = db.select(Showtime).order_by(Showtime.start_time)
    showtimes = db.session.scalars(stmt)
    return showtimes_schema.dump(showtimes), 200

# GET SHOWTIME VIA ID
@showtime_bp.route('/<int:showtime_id>', methods=['GET'])
def get_showtime(showtime_id):
    stmt = db.select(Showtime).filter_by(id=showtime_id)
    showtime = db.session.scalar(stmt)
    if showtime:
        return showtime_schema.dump(showtime), 200
    else:
        return {"error": f"Showtime with id {showtime_id} not found"}, 404

# CREATE SHOWTIME
@showtime_bp.route('/', methods=['POST'])
@role_check('Manager')
def create_showtime():
    # user_id = get_jwt_identity()
    # user = db.session.scalar(db.select(User).filter_by(id=user_id))
    # if user and user.role == 'employee':

    data = request.get_json()
    try:
        # Load data into schema to create a Showtime instance
        showtime_data = ShowtimeSchema().load(data)
        showtime = Showtime(**showtime_data) # ** unpacks the dictionary
        db.session.add(showtime)
        db.session.commit()
        return showtime_schema.dump(showtime), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE SHOWTIME
@showtime_bp.route('/<int:showtime_id>', methods=['PUT', 'PATCH'])
@role_check('Manager')
def update_showtime(showtime_id):
    data = request.get_json()
    stmt = db.select(Showtime).filter_by(id=showtime_id)
    showtime = db.session.scalar(stmt)
    print(data)
    if showtime:
        try:
            showtime_data = ShowtimeSchema(partial=True).load(data)
            for key, value in showtime_data.items():
                setattr(showtime, key, value)
            db.session.commit()
            return showtime_schema.dump(showtime), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Showtime with id {showtime_id} not found"}, 404 

# DELETE SHOWTIME
@showtime_bp.route('/<int:showtime_id>', methods=['DELETE'])
@role_check('Manager')
def delete_showtime(showtime_id):
    stmt = db.select(Showtime).filter_by(id=showtime_id)
    showtime = db.session.scalar(stmt)
    if showtime:
        db.session.delete(showtime)
        db.session.commit()
        return {"message": f"Showtime '{showtime_id}' deleted successfully"}, 200
    else:
        return {"error": f"Showtime with id {showtime_id} not found"}, 404
