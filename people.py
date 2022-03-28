from flask import make_response, abort, jsonify, request
from sqlalchemy.orm import joinedload

from config import db
from models import Person, PersonSchema, Note


def read_all():

    people = Person.query.order_by(Person.lname).all()
    #people = db.session.query(Person).options(joinedload(Person.notes)).all()

    person_schema = PersonSchema(many=True)
    #data = schema.dump(people)

    data = person_schema.dump(people)
    return jsonify(data)


def read_one(person_id):

    #person = Person.query.filter(Person.person_id == person_id).one_or_none()
    person = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        person_schema = PersonSchema()
        #return person_schema.jsonify(person)
        data = person_schema.dump(person)
        return jsonify(data)

    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )


def create(person):

    data = request.get_json()

    # Can we insert this person?
    try:
        new_person = Person(**data)
        person_schema = PersonSchema()
        data = person_schema.dump(person)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response

        return jsonify(data)

    # Otherwise, nope, person exists already
    except Exception as e:
        print(e)
        jsonify({"error": "There was an error please contact the administrator"})


def update(person_id, person):

    data = request.get_json()

    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    update = Person(**data)
    schema = PersonSchema()

    update.person_id = update_person.person_id

    db.session.merge(update)
    db.session.commit()

    data = schema.dump(update)

    return jsonify(data)


def delete(person_id):
    try:
        data = request.get_json()
        person = Person.query.filter_by(person_id=person_id).first()
        person = Person.query.filter_by(person_id=person_id)
        person.delete(data)
        db.session.commit()

        return jsonify(data)
    except Exception as e:
        jsonify({"error": "There was an error please contact the administrator"})  # Routes