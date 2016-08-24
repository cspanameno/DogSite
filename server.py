"""Pet site"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from pet_model import connect_to_db, db, User, Pet, UserPet, Breed, BreedPet

from testsearch import *

import pprint


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("registration_form.html")


@app.route('/register', methods=['POST'])
def process_registration():
    """Process form for the user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")

    user = User.query.filter_by(email=email).first()

    if not user: 
        new_user=User(first_name=first_name, last_name=last_name, email=email, password=password, 
                      zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        print User.user_id
        return redirect("/login")
        
       
    else:
        flash("You already have a profile, please sign in")
        return redirect("/login")


@app.route('/login', methods=['GET'])
def show_login():
    """Show login form"""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def process_login():
    """Process login form"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    print user

    if not user:
        flash("This email does not exist, please register")
        return redirect("/login")

    if user.password != password:
        flash("Wrong password, please try again")
        return redirect("/login")

    else:
        session["user_id"] = user.user_id
        print user.user_id
        flash("Logged in")
        return redirect("/search_form")

@app.route('/logout')
def logout():
    """allow user to log out"""

    del session["user_id"]
    flash("You have been logged out")
    return redirect("/")


@app.route('/profile')
def show_profile():
    """show the user's profile page"""

    user_id = session['user_id']

    #returns a list of objects
    # user_pets = db.session.query(UserPet).filter(UserPet.user_id == user_id).all()

    # pets = []

    # for pet in user_pets:
    #     pets.append(pet.pet_id)

    # select * 
    # FROM pets p 
    # JOIN user_pets up on p.pet_id = up.pet_id
    # WHERE up.user_id = 1;

    # pets = Session.query(UserPet,Pet).filter(UserPet.pet_id == Pet.pet_id).
    # filter(UserPet.user_id == user_id).all()
    
    # print pets
    # one_pet = db.session.query(Pet).filter(Pet.pet_id == pets).all()

    pets = db.session.query(Pet).join(UserPet).filter(UserPet.user_id == user_id).all()

    print pets


    # select * from UserPet where user_id=user_id;

    #need to select all pets from user pet
    # get info for each pet and display 

    return render_template("profile_page.html", pets=pets)


@app.route('/search_form')
def search_form():
    """show the search form"""

    breeds = db.session.query(Breed).all()
    breed_names = []

    for breed in breeds:
        breed_names.append(breed.breed_name)

    return render_template("pet_search_form.html", breeds=breed_names)


@app.route('/search')
def process_form():
    """to process, it is hidden, to call api and get result and render template flask and jinja lecture """
    
    breed = request.args.get("breed")
    age = request.args.get("age")
    size = request.args.get("size")
    gender = request.args.get("gender")
    zipcode = request.args.get("zipcode")

    r = search_dogs_api(breed, age, size, gender, zipcode)

    result = r.json()

    if isinstance(result['petfinder']['pets'].get('pet'), dict):
        pets = [result['petfinder']['pets'].get('pet')]
    else:
        pets = result['petfinder']['pets'].get('pet')

    for pet in pets:
        if type(pet['breeds']['breed']) == type({}):
            pet['breeds']['breed'] = [pet['breeds']['breed']]
        else:
            pet['breeds']['breed'] = pet['breeds']['breed']

    # pprint.pprint(pets)

   
    return render_template("display_pets.html", pets=pets)


@app.route('/idv_pet/<int:id>')
def show_pet(id):
    """show the individual pet"""

    p = get_pet(id)

    pet = p.json()

    pprint.pprint(pet)
    
    if type(pet['petfinder']['pet']['breeds']['breed']) == type({}):
        breeds = [pet['petfinder']['pet']['breeds']['breed']]
    else:
        breeds = pet['petfinder']['pet']['breeds']['breed']


    return render_template("specific_pet.html", pet=pet['petfinder']['pet'], breeds=breeds)



@app.route('/fav', methods=['POST'])
def fav_pet():
    """favorite the pet"""

    api_id = request.form.get('petID')
    age = request.form.get('age')
    breed_names = request.form.get('breed').rstrip(',').split(',')
    name = request.form.get('name')
    size = request.form.get('size')
    zipcode = request.form.get('zipcode')
    photo_url = request.form.get('photo')
    gender = request.form.get('gender')

    user_id = session['user_id']

    print user_id
 
    existing_pet_record = db.session.query(Pet).filter(Pet.api_id == api_id).first()

    if not existing_pet_record:

        pet = Pet(api_id=api_id, age=age, name=name, size=size, zipcode=zipcode, 
                  photo_url=photo_url, gender=gender)

        db.session.add(pet)
        db.session.commit()

        new_pet_id = db.session.query(Pet).filter(Pet.api_id == api_id).one().pet_id

        for breed_name in breed_names:
            breed_id = db.session.query(Breed).filter(Breed.breed_name == breed_name).one().breed_id
            breed_pet = BreedPet(breed_id=breed_id, pet_id=new_pet_id)
            db.session.add(breed_pet)
            db.session.commit()


    pet_record_id = db.session.query(Pet).filter(Pet.api_id == api_id).first().pet_id

    user_pet_record = db.session.query(UserPet).filter(UserPet.pet_id == pet_record_id, UserPet.user_id == user_id).first()

    if user_pet_record:
        print "ALREADY HERE"
    else:
        user_pet = UserPet(user_id=user_id, pet_id=pet_record_id)
        db.session.add(user_pet)
        db.session.commit()


    return jsonify({"status": "success", "petAdded": api_id})



@app.route('/unfav')
def unfav_pet():
    """unfavorite the pet"""

    pass


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")