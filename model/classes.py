# backend (Python) made on a GitHub repository using a teacher template according to their instructions: https://github.com/nighthawkcoders/flask_portfolio
# database dependencies to support sqliteDB
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# this code was mostly written by a collaborator, but I helped alter some of the arguments and added preset data for Grand Wizard
class Classes(db.Model):
    __tablename__ = 'CharClasses'

    # define the schema with the different stats
    id = db.Column(db.Integer, primary_key=True)
    _classname = db.Column(db.String(255), unique=False, nullable=False)
    _health = db.Column(db.Integer, nullable=False)
    _attack = db.Column(db.Integer, nullable=False)
    _range = db.Column(db.Boolean, default=False, nullable=False)
    _movement = db.Column(db.Boolean, default=False, nullable=False)

    # initializes the instance variables within object self
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
            db.session.add(self) # add prepares to persist object to datatable
            db.session.commit() # manual commit
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
            "range": self.range,
            "movement": self.movement
        }

    # CRUD update not used

    # CRUD delete removes self
    # returns None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# make database and datatable
# builds data
def initCharClasses():
    with app.app_context():
        db.create_all()
        # preset class data
        u1 = Classes(classname='Knight', health=2, attack=2, range=False, movement=False)
        u2 = Classes(classname='Mage', health=1, attack=1, range=True, movement=False)
        u3 = Classes(classname='Rogue', health=1, attack=1, range=False, movement=True)
        u4 = Classes(classname='Shield Bearer', health=3, attack=1, range=False, movement=False)
        u5 = Classes(classname='Grand Wizard', health=10, attack=10, range=True, movement=True)
        CharClasses = [u1, u2, u3, u4, u5]

        # builds classes
        for CharClass in CharClasses:
            try:
                CharClass.create()
            except IntegrityError:
                # fails if bad or duplicate data
                db.session.remove()
                print(f"Records exist, duplicate or error: {CharClass.classname}")
            