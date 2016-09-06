"""Add data to PetSite"""

from sqlalchemy import func

from pet_model import User, Pet, UserPet, Breed, BreedPet,  connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    user = User(first_name="Cindy", last_name="P", email="cindy@gmail.com", 
                      password="baba123", zipcode="94621")

    db.session.add(user)
 
    db.session.commit()


# def load_pets():
#     """Load pets into database."""

#     print "Pets"

#     pet = Pet(breed="Chihuaha", size="small",
#                       age="baby",
#                       zipcode="94621")

#         # We need to add to the session or it won't ever be stored
#     db.session.add(pet)

#     #     # provide some sense of progress
#     # if i % 100 == 0:
#     #         print i

#     # Once we're done, we should commit our work
#     db.session.commit()

def load_breeds():
    """Load breeds into database."""

    breeds_file = open('breed_data.txt')

    breeds = breeds_file.read().split(',')

    for breed_name in breeds:
        breed = Breed(breed_name=breed_name)
        db.session.add(breed)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    set_val_user_id()
    load_breeds()
