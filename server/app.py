#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes
def bio_text_for(speaker):
    """Return the speaker's bio text, or a default message if they have none."""
    return speaker.bio.bio_text if speaker.bio else "No bio available"

@app.route('/events')
def get_events():
    events = Event.query.all()
    body = [
        {'id': event.id, 'name': event.name, 'location': event.location}
        for event in events
    ]
    return jsonify(body), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = db.session.get(Event, id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    body = [
        {
            'id': session.id,
            'title': session.title,
            'start_time': session.start_time.isoformat() if session.start_time else None,
        }
        for session in event.sessions
    ]
    return jsonify(body), 200


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    body = [{'id': speaker.id, 'name': speaker.name} for speaker in speakers]
    return jsonify(body), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return jsonify({'error': 'Speaker not found'}), 404

    body = {
        'id': speaker.id,
        'name': speaker.name,
        'bio_text': bio_text_for(speaker),
    }
    return jsonify(body), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = db.session.get(Session, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    body = [
        {
            'id': speaker.id,
            'name': speaker.name,
            'bio_text': bio_text_for(speaker),
        }
        for speaker in session.speakers
    ]
    return jsonify(body), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)