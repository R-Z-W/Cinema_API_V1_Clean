from init import db, ma
from datetime import date
from marshmallow import fields
from marshmallow import validates, ValidationError

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    password = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(100))
    # is_admin = db.Column(db.Boolean, default=False)
    department = db.Column(db.String(100))
    salary = db.Column(db.Float)
    leave = db.Column(db.Float)
    leave_sick = db.Column(db.Float)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    invoices = db.relationship('Invoice', back_populates='employee', cascade='all, delete')

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    invoices = fields.List(fields.Nested('InvoiceSchema'))

    # TODO Sending Post Method Fails As str > date object
    # @validates('dob')
    # def validate_dob(self, value):
    #     if value > date.today():
    #         raise ValidationError("Date of birth cannot be in the future.")

    class Meta:
            fields = ('fname', 'lname', 'password', 'dob', 'email', 'phone', 'role', 'department', 'salary', 'leave', 'leave_sick', 'date_created')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)