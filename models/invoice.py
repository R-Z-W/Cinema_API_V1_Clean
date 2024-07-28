from init import db, ma
from marshmallow import fields

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_delivered = db.Column(db.DateTime)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Relationships
    tickets = db.relationship('Ticket', back_populates='invoice', cascade='all, delete')
    customer = db.relationship('Customer', back_populates='invoices')
    employee = db.relationship('Employee', back_populates='invoices')
    


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    tickets = fields.List(fields.Nested('TicketSchema'), only=['id']) #TODO
    customer = fields.Nested('CustomerSchema', only=['fname', 'lname'])
    employee = fields.Nested('EmployeeSchema', only=['fname', 'lname'])

    class Meta:
        fields = ('total_price', 'status', 'date_created', 'date_delivered', 'customer_id', 'employee_id')

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

