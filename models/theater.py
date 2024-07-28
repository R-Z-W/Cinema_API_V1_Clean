from init import db, ma
from marshmallow import fields

class Theater(db.Model):
    __tablename__ = "theaters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))

    # Relationships
    showtimes = db.relationship('Showtime', back_populates='theater', cascade='all, delete')

class TheaterSchema(ma.SQLAlchemyAutoSchema):
    dob = fields.Date(required=True)
    date_created = fields.DateTime(required=False)
    showtimes = fields.List(fields.Nested('ShowtimeSchema'))

    class Meta:
        fields = ('name', 'location')

theater_schema = TheaterSchema()
theaters_schema = TheaterSchema(many=True)