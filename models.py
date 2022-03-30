from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Integer, ForeignKey
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested


class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = relationship("Note", back_populates='person')


class Note(db.Model):
    __tablename__ = "note"
    note_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.person_id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    person = relationship("Person", back_populates='notes')


class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person

    notes = Nested(lambda: NoteSchema())

class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Note

    person = Nested(lambda: PersonSchema())
