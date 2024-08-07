from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=True)
    tickets = db.relationship('Ticket', backref='participant', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
