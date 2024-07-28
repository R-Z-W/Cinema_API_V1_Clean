from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from init import db, ma
from models.ticket import Ticket, TicketSchema

ticket_bp = Blueprint('ticket', __name__, url_prefix='/tickets')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

# GET ALL TICKETS
@ticket_bp.route('/', methods=['GET'])
def get_all_tickets():
    stmt = db.select(Ticket).order_by(Ticket.name)
    tickets = db.session.scalars(stmt)
    return tickets_schema.dump(tickets), 200

# GET TICKET VIA ID
@ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    stmt = db.select(Ticket).filter_by(id=ticket_id)
    ticket = db.session.scalar(stmt)
    if ticket:
        return ticket_schema.dump(ticket), 200
    else:
        return {"error": f"Ticket with id {ticket_id} not found"}, 404

# CREATE TICKET
@ticket_bp.route('/', methods=['POST'])
#@jwt_required()
def create_ticket():
    # user_id = get_jwt_identity()
    # user = db.session.scalar(db.select(User).filter_by(id=user_id))
    # if user and user.role == 'employee':

    data = request.get_json()
    try:
        # Load data into schema to create a Ticket instance
        ticket_data = TicketSchema().load(data)
        ticket = Ticket(**ticket_data) # ** unpacks the dictionary
        db.session.add(ticket)
        db.session.commit()
        return ticket_schema.dump(ticket), 201
    except Exception as e:
        return {"message": str(e)}, 400

# UPDATE TICKET
@ticket_bp.route('/<int:ticket_id>', methods=['PUT', 'PATCH'])
#@jwt_required()
def update_ticket(ticket_id):
    data = request.get_json()
    stmt = db.select(Ticket).filter_by(id=ticket_id)
    ticket = db.session.scalar(stmt)
    print(data)
    if ticket:
        try:
            ticket_data = TicketSchema(partial=True).load(data)
            for key, value in ticket_data.items():
                setattr(ticket, key, value)
            db.session.commit()
            return ticket_schema.dump(ticket), 201
        except Exception as e:
            return {"message": str(e)}, 400
    else:
        return {"error": f"Ticket with id {ticket_id} not found"}, 404 

# DELETE TICKET
@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
#@jwt_required()
def delete_ticket(ticket_id):
    stmt = db.select(Ticket).filter_by(id=ticket_id)
    ticket = db.session.scalar(stmt)
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        return {"message": f"Ticket '{ticket_id}' deleted successfully"}, 200
    else:
        return {"error": f"Ticket with id {ticket_id} not found"}, 404
