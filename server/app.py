from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    '''Returns a list of all messages in JSON format.'''
    messages = Message.query.all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    '''Creates a new message in the database and returns the created message as JSON.'''
    data = request.get_json()
    new_message = Message(
        body=data['body'],
        username=data['username'],
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    '''Updates the body of a message in the database and returns the updated message as JSON.'''
    data = request.get_json()
    message = Message.query.get_or_404(id)
    if 'body' in data:
        message.body = data['body']
        db.session.add(message)
        db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    '''Deletes a message from the database.'''
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)