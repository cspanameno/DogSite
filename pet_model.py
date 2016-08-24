"""Models and database functions for Petsite project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#####################################################################

class User(db.Model):
    """User of pet site."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)

    pets = db.relationship("Pet",
                         secondary="user_pets",
                         backref="users")

class Pet(db.Model):
    """Pet on pet site"""

    __tablename__ = "pets"

    pet_id= db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    api_id = db.Column(db.String(100))
    name = db.Column(db.String(100))
    size = db.Column(db.String(100))
    age = db.Column(db.String(100))
    zipcode = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(15))
    photo_url = db.Column(db.String(128))

    breeds = db.relationship("Breed",
                         secondary="breed_pets",
                         backref="pets")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Pet pet_id=%s breed=%s>" % (self.pet_id,
                                                 self.breeds)


class UserPet(db.Model):
    """ Association table to relate pet and users"""
   
    __tablename__ = "user_pets"

    fav_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    pet_id= db.Column(db.Integer,
                         db.ForeignKey('pets.pet_id'))

class Breed(db.Model):

    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    breed_name = db.Column(db.String(100))

class BreedPet(db.Model):

    __tablename__ = "breed_pets"

    breed_pet_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    breed_id = db.Column(db.Integer,
                        db.ForeignKey('breeds.breed_id'))
    pet_id = db.Column(db.Integer,
                         db.ForeignKey('pets.pet_id'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_pets user_id=%s pet_id=%s >" % (self.user_id,
                                                 self.pet_id)




# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."