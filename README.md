# web_map
This program is needed for creating map with nearest locations where films were shoted.

## Usage
'''python3 main.py 
Please enter a year you would like to have a map for: 2014
Please enter your location (format: lat long): 49.817906 24.022997
Generating map...
Please wait...
Searched 100 films.....
Searched 200 films.....
Searched 300 films.....
Searched 400 films.....
Searched 500 films.....
Searched 600 films.....
Searched 700 films.....
Searched 800 films.....
Searched 900 films.....
Searched 1000 films.....
Finished. Please have look at the map 2014_movies_map.html
'''

##Description
Firstly, you give the year, when film was filmed.
Secondly, you give your location(in lat and long)
And map will be created named '(year)_movies_map.html'

data_read():
read the data base of films and remove such trash as names of serias in serials and ect.

find_nearest():
use library geopy to find coordinates of places where filmes were made and give 10 neares places.

generate_map():
generate three layers of map:
- countries in different colors depend of number of populatiion
- markers with name of film and place
- the map

##example
This is the map for location (49.817906 24.022997) in 2014:
(open map 2014_1 and 2014_2) In this launch program see only 1000 films from list
For this locations in 2013 but for 10000 for better accuracy:
(open map 2013)
There is a screenshot for input
If you want you can set varieble k(sring 57) to 10000

#All screenshots are in folder#
