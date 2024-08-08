from flask import Flask, jsonify, send_from_directory
from utils.database import db, mongo_db, init_db
from utils.data_loader import load_initial_data
from routes.participant_routes import participant_bp
from routes.event_routes import event_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MONGO_URI"] = "mongodb://localhost:27017/events"


init_db(app)

# Register blueprints
app.register_blueprint(participant_bp)
app.register_blueprint(event_bp)

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')


@app.route('/load_initial_data', methods=['POST'])
def load_initial_data_route():
    load_initial_data()
    return jsonify({'message': 'Initial data loaded successfully!'}), 201

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

