import pandas as pd
from models import Participant, Ticket
from utils.database import db, mongo_db
from sqlalchemy.exc import SQLAlchemyError
import os

def load_events_from_json(file_path):
    events_data = pd.read_json(file_path)
    events_dict = events_data.to_dict(orient="records")
    mongo_db.db.events.insert_many(events_dict)
    print(f"Events added: {len(events_dict)}")

def load_participants_from_csv(file_path, db_session):
    # Read CSV file into a DataFrame
    participants_data = pd.read_csv(file_path)
    
    # Iterate over DataFrame rows
    for index, row in participants_data.iterrows():
        try:
            # Create a new Participant object
            participant = Participant(
                id=row['Id'],
                name=row['Name'],
                country=row['Country']
                # Ensure other fields are handled if required
            )
            # Add the participant to the session
            db_session.add(participant)
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    
    # Commit the session and handle potential errors
    try:
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error committing session: {e}")


def load_tickets_from_csv(file_paths, db_session):
    for file_path in file_paths:
        tickets_data = pd.read_csv(file_path)
        for index, row in tickets_data.iterrows():
            try:
                ticket = Ticket(
                    user_id=int(row['user_id']),
                    event_id=int(row['event_id'])
                )
                db_session.add(ticket)
                print(f"Ticket added from {file_path}: {index} {ticket}")
            except Exception as e:
                print(f"Error processing row {index} in {file_path}: {e}")
    try:
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error committing session: {e}")

def load_tickets_from_directory(directory, db_session):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            load_tickets_from_csv([file_path], db_session)

def init_session():
    # Create a session object
    session = db.session()

    # Return the session object
    return session

def load_initial_data():
    session = init_session()
    load_events_from_json('data/events_taylor.json')
    load_events_from_json('data/events_metallica.json')
    load_participants_from_csv('data/users.csv', session)
    load_tickets_from_directory('data/tickets', session)