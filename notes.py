from flask import make_response, abort, jsonify, request
from config import db
from models import Person, Note, NoteSchema


def read_all():
    notes = Note.query.order_by(db.desc(Note.timestamp)).all()

    note_schema = NoteSchema(many=True)

    data = note_schema.dump(notes)
    return jsonify(data)


def read_one(person_id, note_id):
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Person.person_id == person_id)
            .filter(Note.note_id == note_id)
            .one_or_none()
    )

    note_schema = NoteSchema()
    data = note_schema.dump(note)
    return jsonify(data)


def create(person_id, note):
    data = request.get_json()
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Can we insert this person?
    try:
        new_note = Note(**data)
        note_schema = NoteSchema()

        # schema = NoteSchema()
        # new_note = schema.load(note).data

        # Add the person to the database
        person.notes.append(new_note)
        db.session.commit()

        data = schema.dump(new_note)

        return jsonify(data)

    # Otherwise, nope, person exists already
    except Exception as e:
        print(e)
        jsonify({"error": "There was an error please contact the administrator"})


def update(person_id, note_id, note):
    data = request.get_json()
    update_note = Note.query.filter(Person.person_id == person_id).filter(Note.note_id == note_id).one_or_none()

    update = Note(**data)
    note_schema = NoteSchema()


    update.person_id = update_note.person_id
    update.note_id = update_note.note_id

    db.session.merge(update)
    db.session.commit()

    data = note_schema.dump(update)

    return jsonify(data)


def delete(person_id, note_id):
    note = Note.query.filter(Person.person_id == person_id).filter(Note.note_id == note_id).one_or_none()

    db.session.delete(note)
    db.session.commit()

    return make_response(
        "Note {note_id} deleted".format(note_id=note_id), 200
    )
