#! /usr/bin/env python
# -*- coding: utf-8 -*-
import folium
from haversine import haversine
from pprint import pprint
from geopy.geocoders import Nominatim


def request():
    """
    void -> (str, (int, int))
    Ask user to enter year of film and cordinates of his position
    """
    year = input("Please enter a year you would like to have a map for: ")
    while year.isdigit() is False or int(year) > 2020 or int(year) < 1900:
        year = input("Please enter a year you would like to have a map for: ")
    lat, lon = input("Please enter your location (format: lat long): ").split()
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        print('lat and long must be float')
        lat, lon = input("Please enter your location (format: lat long): ").split()
        lat = float(lat)
        lon = float(lon)
    while lon < 0 or lon > 180 or lat < -90 or lat > 90:
        lat, lon = input("Please enter your location (format: lat long): ").split()
        lat = float(lat)
        lon = float(lon)

    print("Generating map...")
    print("Please wait...")
    return (year, (int(lat), int(lon)))
# print(request())

def data_read(filename):
    """
    str -> lst
    Return list of films from file 'filename'
    Returning will be: ['name of film', 'year', 'place']
    """
    if type(filename) != str:
        return None
    lst = []
    movie_names = []
    s = '' # a name of movie
    c = '' # a name of place or country
    k = 0
    with open(filename, encoding = 'utf-8', errors='ignore') as f:
        for line in f:
            if len(line) > 1:
                if line.strip().split()[0][0] not in ' " ':
                    pass
                else:
                    if k % 100 == 0 and k != 0:
                        print("Searched", k, "films.....")
                    if k > 10000:
                        return lst
                    k += 1
                    line = line.strip().split()
                    for i in line:
                        if i[0] == '(':
                            z = line.index(i)
                            line = line[z:]
                            break
                        s += i + ' '
                    s = s.strip()
                    line.insert(0, s)
                    for p in line:
                        if p[0] == "{":
                            x = line.index(p)
                        if p[-1] == "}":
                            y = line.index(p)
                            del line[x:y + 1]

                    for t in line[2:]:
                        if '(' in t:
                            z = line.index(t)
                            line = line[:z]
                            break
                        c += t + ' '
                    line = line[:2]
                    c = c.strip()
                    if "," not in c:
                        continue
                    line.append(c)
                    movie_names.append(s)
                    if line not in lst:
                        lst.append(line)
                    s = ''
                    c = ''
        print("\n")
    return lst
# pprint(data_read('locations.list'))


def find_nearest(year, your_loc, films):
    """
    str, (int, int), lst -> lst
    Find the nearest shot muvie to your location in chosen year
    Distance in km
    >>> find_nearest('2014', (49.817906, 24.022997), data_read('test.list'))

    """
    distances = []
    locations = []
    for film in films:
        if film[1] == "(" + year + ")":
            try:
                geolocator = Nominatim(user_agent = "specify_your_app_name_here")
                location = geolocator.geocode(film[-1])
                loc_city = (location.latitude, location.longitude)
                distance = haversine(your_loc, loc_city)
                distances.append((film[0], film[2], loc_city, distance))
                distances.sort(key = lambda distance: distance[3])
            except:
                pass
    for d in distances:
        locations.append((d[0], d[1], d[2]))
    return locations[:10]
# pprint(find_nearest("2014", (49.817906, 24.022997), data_read('locations.list')))


def generate_map(locations, year, your_loc):
    """
    lst -> file
    Return html with map with the nearest places where films was shoted
    """
    lat = your_loc[0]
    lon = your_loc[1]
    map = folium.Map(location = [lat, lon], zoom_start = 10)
    fg_marker = folium.FeatureGroup(name = 'Film_layer')
    for city in locations:
        lt = city[-1][0]
        ln = city[-1][1]
        name = city[0]
        c = city[1]
        fg_marker.add_child(folium.Marker(location = [lt, ln], popup = c + "\n\n" + name, icon = folium.Icon()))

    fg_country = folium.FeatureGroup(name = 'Country_layer')
    fg_country.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), \
    style_function = lambda x: {'fillColor':'green' \
    if x['properties']['POP2005'] < 10000000 \
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 \
    else 'red'}))

    map.add_child(fg_marker)
    map.add_child(fg_country)
    map.add_child(folium.LayerControl())
    file = year + '_movies_map.html'
    map.save(file)
    print('Finished. Please have look at the map ' + file)
# generate_map(find_nearest("2014", (49.817906, 24.022997), data_read('locations.list')), "2014")
# generate_map(find_nearest("2014", (38.340272, -99.568177), data_read('locations.list')), "2014")


def main():
    """
    void -> html
    Make map in browser of places where nearest to your film was filmed.
    Here user gives information and gets map
    """
    inform = request()
    year = inform[0]
    cord = inform[1]
    films = data_read('locations.list')
    locations = find_nearest(year, cord, films)
    generate_map(locations, year, cord)
main()
