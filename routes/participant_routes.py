from flask import Blueprint, request, jsonify
from models import Participant, db

participant_bp = Blueprint('participant_bp', __name__)

@participant_bp.route('/participants', methods=['POST'])
def add_participant():
    data = request.get_json()
    participant = Participant(
        id=data['Id'],
        name=data['Name'],
        country=data['Country']
    )
    db.session.add(participant)
    db.session.commit()
    return jsonify({'message': 'Participant added successfully!'}), 201

@participant_bp.route('/participants', methods=['GET'])
def get_participants():
    participants = Participant.query.all()
    return jsonify([p.to_dict() for p in participants])
