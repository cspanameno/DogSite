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







# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     for i, row in enumerate(open("seed_data/u.data")):
#         row = row.rstrip()

#         user_id, movie_id, score, timestamp = row.split("\t")

#         user_id = int(user_id)
#         movie_id = int(movie_id)
#         score = int(score)

#         # We don't care about the timestamp, so we'll ignore this

#         rating = Rating(user_id=user_id,
#                         movie_id=movie_id,
#                         score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#         # provide some sense of progress
#         if i % 1000 == 0:
#             print i

#             # An optimization: if we commit after every add, the database
#             # will do a lot of work committing each record. However, if we
#             # wait until the end, on computers with smaller amounts of
#             # memory, it might thrash around. By committing every 1,000th
#             # add, we'll strike a good balance.

#             db.session.commit()

#     # Once we're done, we should commit our work
#     db.session.commit()


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
