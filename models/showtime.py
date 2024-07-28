from init import db, ma
from datetime import datetime, timedelta
from marshmallow import fields
from marshmallow import validates, ValidationError

class Showtime(db.Model):
    __tablename__ = "showtimes"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    # Foreign keys
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    # Relationships
    theater = db.relationship('Theater', back_populates='showtimes')
    movie = db.relationship('Movie', back_populates='showtimes')
    tickets = db.relationship('Ticket', back_populates='showtime', cascade='all, delete')

class ShowtimeSchema(ma.SQLAlchemyAutoSchema):
    movie = fields.Nested('MovieSchema')
    theater = fields.Nested('TheaterSchema')
    tickets = fields.List(fields.Nested('TicketSchema'))

    def validate_times(self, data, **kwargs):
        start_time = data['start_time']
        end_time = data['end_time']
        movie_runtime = data['movie'].runtime  # Assuming runtime is in minutes

        if end_time <= start_time:
            raise ValidationError("End time must be after start time.")

        required_end_time = start_time + timedelta(minutes=movie_runtime)
        if end_time < required_end_time:
            raise ValidationError(f"End time must be at least {movie_runtime} minutes after start time.")


    class Meta:
        fields = ('start_time', 'end_time', 'date_created', 'theater_id', 'movie_id')

showtime_schema = ShowtimeSchema()
showtimes_schema = ShowtimeSchema(many=True)