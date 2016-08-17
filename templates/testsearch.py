import requests
from pprint import pprint



def print_emp(location, breed, gender):
    """Print detail about an employee."""

    print
    print label
    print

    pets = requests.get(
        "http://www.petfinder.com/pet-search?location=%s&animal=dog&breed=%s&gender=%s".json()
    
    pprint(emp, width=40, indent=2)

    print
    raw_input("=====")

print_emp("94621", "chihuahua", "female")
