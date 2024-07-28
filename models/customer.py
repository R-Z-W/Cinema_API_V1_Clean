from init import db, ma
from datetime import date
from marshmallow import fields
from marshmallow import validates, ValidationError

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    # password = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    invoices = db.relationship('Invoice', back_populates='customer', cascade='all, delete')

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    invoices = fields.List(fields.Nested('InvoiceSchema'))


    # TODO Sending Post Method Fails As str > date object 
    # @validates('dob')
    # def validate_dob(self, value):
    #     if value > date.today():
    #         raise ValidationError("Date of birth cannot be in the future.")


    class Meta:
        fields = ('fname', 'lname', 'dob', 'email', 'phone', 'date_created')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
