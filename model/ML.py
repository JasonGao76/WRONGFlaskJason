# backend (Python) made on a GitHub repository using a teacher template according to their instructions: https://github.com/nighthawkcoders/flask_portfolio
from sqlalchemy import Column, Integer, String, Float
from __init__ import db

# the below code is a combination of teacher code (from a lesson on machine learning using the Titanic dataset) and our adaption of that code to use in this project
class ML(db.Model):
    __tablename__ = "ml"

    # define the schema with the inputs to feed into the machine learning (ml)
    id = Column(Integer, primary_key=True)
    _socialclass = Column(Integer, nullable=False)
    _age = Column(Integer, nullable=False)
    _sex = Column(String, nullable=False)
    _siblings = Column(Integer, nullable=False)
    _family = Column(Integer, nullable=False)
    _fare = Column(Integer, nullable=False)
    _port = Column(String, nullable=False)
    _alone = Column(String, nullable=False)

    # initializes the instance variables within object (self)
    def __init__(self, socialclass, age, sex, siblings, family, fare, port, alone):
        self._socialclass = socialclass
        self._age = age
        self._sex = sex
        self._siblings = siblings
        self._family = family
        self._fare =  fare
        self._port = port
        self._alone = alone
    
    def __repr__(self):
        return "id='%s', socialclass='%d', age='%d', sex='%s', siblings='%d', family='%d', fare='%d', port='%s', alone='%s'" % (self.id, self.socialclass, self.age, self.sex, self.siblings, self.family, self.fare, self.port, self.alone)

    # property and setter for all arguments
    @property
    def socialclass(self):
        return self._socialclass
    
    @socialclass.setter
    def socialclass(self, value):
        self._socialclass = value
        
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
    
    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, value):
        self._sex = value
    
    @property
    def siblings(self):
        return self._siblings
    
    @siblings.setter
    def siblings(self, value):
        self._siblings = value
        
    @property
    def family(self):
        return self._family
    
    @siblings.setter
    def family(self, value):
        self._family = value
        
    @property
    def fare(self):
        return self._fare
    
    @siblings.setter
    def fare(self, value):
        self._fare = value
        
    @property
    def port(self):
        return self._port
    
    @siblings.setter
    def port(self, value):
        self._port = value    
        
    @property
    def alone(self):
        return self._alone
    
    @alone.setter
    def alone(self, value):
        self._alone = value

    def to_dict(self):
        return {"id": self.id}
    
def init_ml():
    db.session.commit() # commit database
