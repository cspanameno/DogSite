import requests
import pprint
import json

import os

api_key = os.environ["API_KEY"]


def get_breeds():
    """gets the breed list"""

    breeds = requests.get("http://api.petfinder.com/breed.list?key=" + api_key + "&animal=dog&format=json")

    b = breeds.json()


    return b



def save_breeds():

    b = get_breeds()
    #This returns a dictionary

    breeds = b["petfinder"]["breeds"]["breed"]
    #This gets the values, since it a nested dictionary I moved to the breeds sections

    breeds_list = []
    #created an empty list to add the values from the dictionary

    for breed in breeds:
        breeds_list.append(breed['$t'])
    #This will append a the values to my empty list

    return breeds_list


    # breeds_string = ",".join(breeds_list)
    #Joins the breed_list with a comma seperator

    # with open('breed_data.txt', 'w') as outfile:
    #     outfile.write(breeds_string)
    #sends the breeds_string to a tezt file in my directory

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(breeds)

    # print type(b)

def search_dogs_api(breed, age, size, gender, zipcode):

    api_key = os.environ["API_KEY"]

    payload = {'breed': breed, 'age': age, 'size':size, 'sex':gender, 'location':zipcode, 'key': api_key, 'format': 'json' }


    dogs = requests.get("http://api.petfinder.com/pet.find", params=payload)
    

    
    return dogs

def get_pet(id):

    print id

    api_key = os.environ["API_KEY"]

    payload = {'id': id, 'format': 'json', 'key': api_key}
    dog = requests.get("http://api.petfinder.com/pet.get", params=payload)

    return dog
# search_dogs_api()





