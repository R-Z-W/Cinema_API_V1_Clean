from init import db, ma
from marshmallow import fields
from marshmallow import validates, ValidationError

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    plot = db.Column(db.Text)
    language = db.Column(db.String(50))
    rating = db.Column(db.Float)

    # Relationships
    showtimes = db.relationship('Showtime', back_populates='movie', cascade='all, delete')

class MovieSchema(ma.Schema):
    
    showtimes = fields.List(fields.Nested('ShowtimeSchema'))

    class Meta:
        fields = ('title', 'year', 'runtime', 'genre', 'director', 'plot', 'language', 'rating')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)