from init import db, ma
from marshmallow import fields
from marshmallow import validates, ValidationError

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    seat_number = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

    # Foreign keys
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))

    # Relationships
    showtime = db.relationship('Showtime', back_populates='tickets')
    invoice = db.relationship('Invoice', back_populates='tickets')

class TicketSchema(ma.SQLAlchemyAutoSchema):

    showtime = fields.Nested('ShowtimeSchema')
    invoice = fields.Nested('InvoiceSchema')

    @validates('price')
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price must be non-negative.")

    @validates('seat_number')
    def validate_seat_number(self, value):
        if not value:
            raise ValidationError("Seat number cannot be empty.")

    class Meta:
        fields = ('price', 'seat_number', 'date_created', 'invoice_id', 'showtime_id')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

