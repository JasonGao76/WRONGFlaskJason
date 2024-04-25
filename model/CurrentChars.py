# database dependencies to support sqliteDB examples
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# this code was written by a collaborator
class CurrentChar(db.Model):
    __tablename__ = 'CurrentChar'

    # define the schema with the different stats
    id = db.Column(db.Integer, primary_key=True)
    _classname = db.Column(db.String(255), unique=False, nullable=False)
    _health = db.Column(db.Integer, nullable=False)
    _attack = db.Column(db.Integer, nullable=False)
    _range = db.Column(db.Boolean, default=False, nullable=False)
    _movement = db.Column(db.Boolean, default=False, nullable=False)

    # initializes the instance variables within object (self)
    def __init__(self, classname, health, attack, range, movement):
        self._classname = classname # variables with self prefix become part of the object
        self._health = health
        self._attack = attack
        self._range = range
        self._movement = movement

    # a name getter method, extracts classname from object
    @property
    def classname(self):
        return self._classname
    
    # a setter function, allows classname to be updated after initial object creation
    @classname.setter
    def classname(self, classname):
        self._classname = classname
    
    # repeat for all arguments
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health
        
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, attack):
        self._attack = attack

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range):
        self._range = range

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, movement):
        self._movement = movement
    
    # output content using str(object) and json dumps so ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create adds a new record to the table
    # returns self or None if error
    def create(self):
        try:
            # creates an object
            db.session.add(self)  # add prepares to persis  object to datatable
            db.session.commit()  # manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "classname": self.classname,
            "health": self.health,
            "attack": self.attack,
            "range": self._range,
            "movement": self.movement,
        }

    # CRUD update
    # returns self
    def update(self, classname="", health=None, attack=None, range=None, movement=None):
        # only updates values with length
        if len(classname) > 0:
            self.classname = classname
            self.health = health
            self.attack = attack
            self._range = range
            self.movement = movement
        db.session.commit()
        return self

    # CRUD delete removes self
    # returns None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# makes database and datatable
# builds data
def initCurrentChars():
    with app.app_context():
        db.create_all()
        # placeholder for current character
        u1 = CurrentChar(classname='', health=None, attack=None, range=None, movement=None)

        CurrentCharacter = [u1]

        # builds the placeholder
        for CurrentCharacter in CurrentCharacter:
            try:
                # add placeholder to table
                CurrentCharacter.create()
            except IntegrityError:
                # fails with bad or duplicate data
                db.session.remove()
                print(f"Records exist, duplicate or error: {CurrentCharacter.classname}")
            