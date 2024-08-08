from flask import Blueprint, request, jsonify
from utils.database import mongo_db, db
from bson import ObjectId
from models import Ticket
from sqlalchemy.orm import joinedload
#from utils.data_loader import get_tickets_by_event

event_bp = Blueprint('event_bp', __name__)

@event_bp.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    mongo_db.db.events.insert_one(data)
    return jsonify({'message': 'Event added successfully!'}), 201

@event_bp.route('/events', methods=['GET'])
def get_events():
    events = list(mongo_db.db.events.find())
    for event in events:
        event['_id'] = str(event['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(events)

@event_bp.route('/events/<string:mongo_id>', methods=['GET'])
def get_event_detail(mongo_id):
    try:
        event = mongo_db.db.events.find_one({'_id': ObjectId(mongo_id)})
        if not event:
            return jsonify({'message': 'Event not found'}), 404

        event_id = event.get('event_id')
        if event_id is None:
            return jsonify({'message': 'Event ID not found in MongoDB document'}), 404

        # Fetch tickets for the event from the relational database
        tickets = get_tickets_by_event(event_id)

        event_detail = {
            'main_attraction': event.get('main_attraction'),
            'Date': event.get('Date'),
            'City': event.get('City'),
            'Country': event.get('Country'),
            'ticket_count': len(tickets),
            'buyers': tickets
        }
        return jsonify(event_detail)

    except Exception as e:
        print(f"Error retrieving event detail for {mongo_id}: {e}")
        return jsonify({'message': 'An error occurred'}), 500

def get_tickets_by_event(event_id):
    try:
        tickets = db.session.query(Ticket).filter(Ticket.event_id == event_id).options(joinedload(Ticket.participant)).all()
        
        ticket_details = []
        for ticket in tickets:
            participant = ticket.participant
            ticket_details.append({
                'name': participant.name if participant else 'Unknown'
            })

        return ticket_details

    except Exception as e:
        print(f"Error retrieving tickets for event {event_id}: {e}")
        return []




