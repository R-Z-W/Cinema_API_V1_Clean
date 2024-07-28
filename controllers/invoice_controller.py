from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from init import db, ma
from models.invoice import Invoice, InvoiceSchema

invoice_bp = Blueprint('invoice', __name__, url_prefix='/invoices')

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

# GET ALL INVOICES
@invoice_bp.route('/', methods=['GET'])
def get_all_invoices():
    stmt = db.select(Invoice).order_by(Invoice.date_created)
    invoices = db.session.scalars(stmt)
    return invoices_schema.dump(invoices), 200

# GET INVOICE VIA ID
@invoice_bp.route('/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    stmt = db.select(Invoice).filter_by(id=invoice_id)
    invoice = db.session.scalar(stmt)
    if invoice:
        return invoice_schema.dump(invoice), 200
    else:
        return {"error": f"Invoice with id {invoice_id} not found"}, 404

# CREATE INVOICE
@invoice_bp.route('/', methods=['POST'])
#@jwt_required()
def create_invoice():
    # user_id = get_jwt_identity()
    # user = db.session.scalar(db.select(User).filter_by(id=user_id))
    # if user and user.role == 'employee':

    data = request.get_json()
    try:
        # Load data into schema to create a Invoice instance
        invoice_data = InvoiceSchema().load(data)
        invoice = Invoice(**invoice_data) # ** unpacks the dictionary
        db.session.add(invoice)
        db.session.commit()
        return invoice_schema.dump(invoice), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE INVOICE
@invoice_bp.route('/<int:invoice_id>', methods=['PUT', 'PATCH'])
#@jwt_required()
def update_invoice(invoice_id):
    data = request.get_json()
    stmt = db.select(Invoice).filter_by(id=invoice_id)
    invoice = db.session.scalar(stmt)
    print(data)
    if invoice:
        try:
            invoice_data = InvoiceSchema(partial=True).load(data)
            for key, value in invoice_data.items():
                setattr(invoice, key, value)
            db.session.commit()
            return invoice_schema.dump(invoice), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Invoice with id {invoice_id} not found"}, 404 

# DELETE INVOICE
@invoice_bp.route('/<int:invoice_id>', methods=['DELETE'])
#@jwt_required()
def delete_invoice(invoice_id):
    stmt = db.select(Invoice).filter_by(id=invoice_id)
    invoice = db.session.scalar(stmt)
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        return {"message": f"Invoice '{invoice_id}' deleted successfully"}, 200
    else:
        return {"error": f"Invoice with id {invoice_id} not found"}, 404
