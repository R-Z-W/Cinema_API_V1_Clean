from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.employee import Employee
from init import db

def role_check(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.scalar(db.select(Employee).filter_by(id=user_id, role=role))
            if not user:
                return ({"error": "Unauthorized"}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator