from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.movie import Movie, MovieSchema
from init import db
from utils import fetch_movie_data
from decorator import role_check

movie_bp = Blueprint('movie', __name__, url_prefix='/movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# GET ALL MOVIES
@movie_bp.route('/', methods=['GET'])
@role_check('Manager') # Hide New Movies From Customers
def get_all_movies():
    stmt = db.select(Movie).order_by(Movie.year)
    movies = db.session.scalars(stmt)
    return movies_schema.dump(movies), 200

# GET MOVIE VIA ID
@movie_bp.route('/<int:movie_id>', methods=['GET'])
@role_check('Manager')
def get_movie(movie_id):
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        return movie_schema.dump(movie), 200
    else:
        return {"error": f"Movie with id {movie_id} not found"}, 404

# CREATE MOVIE
@movie_bp.route('/', methods=['POST'])
@role_check('Manager')
def create_movie():
    data = request.get_json()
    try:
        # Load data into schema to create a Movie instance
        movie_data = MovieSchema().load(data)
        movie = Movie(**movie_data) # ** unpacks the dictionary
        db.session.add(movie)
        db.session.commit()
        return movie_schema.dump(movie), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE MOVIE
@movie_bp.route('/<int:movie_id>', methods=['PUT', 'PATCH'])
@role_check('Manager')
def update_movie(movie_id):
    data = request.get_json()
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    print(data)
    if movie:
        try:
            movie_data = MovieSchema(partial=True).load(data)
            for key, value in movie_data.items():
                setattr(movie, key, value)
            db.session.commit()
            return movie_schema.dump(movie), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Movie with id {movie_id} not found"}, 404 

# DELETE MOVIE
@movie_bp.route('/<int:movie_id>', methods=['DELETE'])
@role_check('Manager')
def delete_movie(movie_id):
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return {"message": f"Movie '{movie_id}' deleted successfully"}, 200
    else:
        return {"error": f"Movie with id {movie_id} not found"}, 404
