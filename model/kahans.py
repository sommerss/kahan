""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json


from __init__ import app, db


from sqlalchemy.exc import IntegrityError



''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Kahans(db.Model):
    __tablename__ = 'kahans'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _song = db.Column(db.String(255), unique=False, nullable=False)
    _tID = db.Column(db.String(255), unique=False, nullable=False)
    _rID = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, song, tID, rID):
        self._song = song    # variables with self prefix become part of the object, 
        self._tID = tID
        self._rID= rID
        
        

    # a name getter method, extracts name from object
    @property
    def song(self):
        return self._song
    
    # a setter function, allows name to be updated after initial object creation
    @song.setter
    def name(self, song):
        self._song = song
    
    # a getter method, extracts email from object
    @property
    def tID(self):
        return self._tID
    
    # a setter function, allows name to be updated after initial object creation
    @tID.setter
    def tID(self, tID):
        self._tID = tID
        
   
    

    
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def rID(self):
        return self._rID
    
    # a setter function, allows name to be updated after initial object creation
    @rID.setter
    def rID(self, rID):
        self._rID = rID



    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "song": self.song,
            "tID": self.tID,
            
            "rID": self.rID
            
           
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, song="", tID="", rID=""):
        """only updates values with length"""
        if len(song) > 0:
            self.song = song
        if len(tID) > 0:
            self.tID = tID
        if len(rID) > 0:
            self.rID = rID
        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initKahans():
    with app.app_context():
        
        
        db.create_all()
    
        k1 = Kahans(song='stick season', tID='2min', rID = 6)
        k2 = Kahans(song='new perspective', tID='3min', rID = 2)
        k3 = Kahans(song="all my love", tID="4min", rID=1)
      
       

        kahans = [k1, k2, k3]

        
        for kahan in kahans:
            try:
                 '''add user/post data to table'''
                 kahan.create()
            except IntegrityError:
                 '''fails with bad or duplicate data'''
                 db.session.remove()
                 print(f"Duplicate email, or error")