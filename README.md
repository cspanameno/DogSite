![DogSite](/graphics/dogsite.png)

DogSite allows users to browse adoptable dogs in their area by filtering by dog breed, size, age, and zipcode. The application analyzes data from the Petfinder API and provides information about their medical record, shelter, and behavior.The app also integrates the Google Maps API to allow users to easily identify nearby dogs and shelters.  When logged in, users can save dog listings to their favorites for later reviewing.  

According to the ASPCA, approximately 3.9 million dogs enter shelters in the United States. DogSite allows users to browse dogs with breeders, rescues, and shelters with ease to increase chances of adiption. 


## Table of Contents
* [Technologies used](#technologiesused)
* [How it works](#how)
* [Version 2.0](#v2)
* [Author](#author)


## <a name="technologiesused"></a>Technologies Used
* Python
* JavaScript + jQuery
* PostgreSQL + SQLAlchemy
* Flask
* Jinja
* AJAX + JSON
* HTML + CSS
* Bootstrap
* Google Maps API
* Petfinder API

## <a name="how"></a>Walk Through

####Login 
The users can register or login from the homepage. Signing up allows the user's information to be saved in the Postgres database using SQLAlchemy and allows them to save their favorite pets for later vieweing.

![Login](/graphics/homepage.png)

####Search Form
After signing in, users are directed to a search form to filter by dog criteria including breed, size, age, gender, and zipcode. When the user clicks submit the values are sent to the Flask server app that then makes an API call to the Petfinder API. The response is then normalized in the server and displayed using Jinja on the following page. 

![Search Form](/graphics/search_form.png)

####Dog Matches and Map
The page displays the results provided by the API, and also has Google Maps API integrated to show the location for each pet. The user has the option to favorite the pet via the favorite button. An event listener then sends the pet information to the server app where SQLAlchemy is used to save the information in the Postgres Database. 

![Dog Matches](/graphics/display_pets.png)

####Favorites
After a user favorites a dog they can view all favorite pets under the favorite tab for later reviewing.   

![Favorites](/graphics/favorites.png)

####Additional Dog Information
where they can also click on a picture to view additional information about the dog such as address, breeds (if mixed), and description. The additional information is obtained by sending another API call to the Petfinder API using a different method.

![Additional Dog Information](/graphics/additional_info.png)


## <a name="v2"></a>Version 2.0

Further features would focus on providing new pet parents tutorials, and help with their new pet. Aditionally, the project could be integrated with social media such as facebook to not only share favorite dogs but also reccomend


## <a name="author"></a>Author
Cindy graduated from UCLA with a BA in Comparative Literature with an emphasis on English and Spanish literature. While in college, she also completed the pre-health curriculum that included mathematics, and physics courses. Prior to Hackbright, she worked as a Product Specialist at Turnitin, an education technology company in Oakland. In her role, she was responsible for troubleshooting bugs reported by customers using Splunk, Zabbix, and Datadog, and for finding underlying issues by using PSQL to query the database. After working closely with engineers and becoming excited about programming, she committed to making software engineering her career, in order to not only investigate underlying issues with the product but also find solutions. 