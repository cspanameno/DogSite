"""Pet site"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from pet_model import connect_to_db, db, User, Pet, User_pet

from testsearch import *

import pprint


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


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
        return redirect("/search_form")
       
    else:
        flash("You already have a profile, please sign in")
        return redirect("/login")


@app.route('/login', methods=['GET'])
def show_login():
    """Show login form"""

    print "HEY"

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def process_login():
    """Process login form"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    print user
    print "HELLO"

    if not user:
        flash("This email does not exist, please register")
        return redirect("/login")

    if user.password != password:
        flash("Wrong password, please try again")
        return redirect("/login")

    else:
        session["user_id"] = user.user_id
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

    pass


@app.route('/search_form')
def search_form():
    """show the search form"""

    breeds = save_breeds()

    return render_template("pet_search_form.html", breeds=breeds)


@app.route('/search')
def process_form():
    """to process, it is hidden, to call api and get result and render template flask and jinja lecture """
    
    breed = request.args.get("breed")
    age = request.args.get("age")
    size = request.args.get("size")
    gender = request.args.get("gender")
    zipcode = request.args.get("zipcode")

    r = search_dogs_api(breed, age, size, gender, zipcode)

    pets = r.json()
    pprint.pprint(pets)

    return render_template("display_pets.html", pets=pets['petfinder']['pets']['pet'])


    
    return render_template("results.html")

@app.route('/idv_pet/<int:id>')
def show_pet(id):
    """show the individual pet"""

    p = get_pet(id)

    pet = p.json()


    return render_template("specific_pet.html", pet=pet['petfinder']['pet'])



@app.route('/fav')
def fav_pet():
    """favorite the pet"""

    pass

@app.route('/unfav')
def unfav_pet():
    """unfavorite the pet"""

    pass


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")