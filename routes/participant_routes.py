from flask import Blueprint, request, jsonify
from models import Participant, Ticket
from utils.database import db
import pandas as pd
import os

participant_bp = Blueprint('participant_bp', __name__)

@participant_bp.route('/participants', methods=['POST'])
def add_participant():
    csv_file = request.files.get('file')
    if not csv_file:
        return jsonify({'message': 'No file provided'}), 400

    participants_data = pd.read_csv(csv_file)
    participants = []
    
    for index, row in participants_data.iterrows():
        participant = Participant(
            id=row['Id'],
            name=row['Name'],
            country=row['Country']
        )
        participants.append(participant)
    
    db.session.bulk_save_objects(participants)
    db.session.commit()
    return jsonify({'message': 'Participants added successfully!'}), 201

@participant_bp.route('/participants', methods=['GET'])
def get_participants():
    participants = Participant.query.all()
    return jsonify([p.to_dict() for p in participants])
