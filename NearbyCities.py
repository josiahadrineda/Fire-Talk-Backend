"""Distance formula may have some degree of error with regards to actual
distance in mi and km, however, the nearest cities should still be accurate!!!
Also note that many minor cities might not be included within the csv."""

import pandas as pd
from geopy.geocoders import Nominatim
from collections import OrderedDict
from math import sqrt, sin, cos, atan2, radians

from AQI import *

# Basic formatting
cities = pd.read_csv('worldcities.csv', sep=',')

# Also for use in app.py
cities_list = list(cities['city'])

def nearby_cities(city, n):
    """Returns the CITY and the nearest N cities, as well as their
    geopoints (coordinates) and AQIs.
    """
    assert n > 0, 'N must be a positive integer.'
    
    global cities

    try:
        # Determine the coordinates of CITY
        geolocator = Nominatim(user_agent="Fire Watch")
        location = geolocator.geocode(city)
        lat, long = location.latitude, location.longitude

        # Sort city.csv by distance from CITY
        cities = cities.sort_values('geopoint', key=distance(lat, long))
        
        # CITY is most likely to be in nearby_cities, so one extra city may be needed.
        nearby_cities = cities.head(n+1)

        nearby_cities_list = list(nearby_cities['city'])
        nearby_cities_geos = list(nearby_cities['geopoint'])
        nearby_cities_dists_list = list(zip(nearby_cities['city'], nearby_cities['distance']))
        
        if city in nearby_cities_list:
            c = nearby_cities_dists_list.pop(nearby_cities_list.index(city))
        else:
            nearby_cities_dists_list.pop()
        nearby_cities_dists_list.insert(0, (city, (0.0, 0.0)))

        # AQI
        nearby_cities_states = list(nearby_cities['admin_name'])
        nearby_cities_countries = list(nearby_cities['country'])
        for i in range(len(nearby_cities_dists_list)):
            ci, st, co = nearby_cities_list[i], nearby_cities_states[i], nearby_cities_countries[i]
            _, dist = nearby_cities_dists_list[i]
            nearby_cities_dists_list[i] = (ci, (get_aqi(ci, st, co), dist))
        
        # Aggregation of data
        city_info = OrderedDict()
        city_info['geos'] = nearby_cities_geos
        city_info['dists'] = nearby_cities_dists_list
        return city_info
    except AttributeError:
        return 'An unexpected error occurred! Try again.'

def distance(lat, long):
    """Takes the reference latitude LAT and longitude LONG and
    returns a calculate_distance function used to sort cities.csv.
    """
    global cities

    lat, long = radians(lat), radians(long)

    #Haversine Formula
    def calculate_distance_haversine(geopoint):
        dists = []
        for gp in geopoint:
            lat2, long2 = convert_str_to_gp(gp)
            y = radians(lat2 - lat)
            x = radians(long2 - long)

            a = sin(y/2)**2 + cos(lat) * cos(lat2) * sin(x/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))

            R_mi, R_km = 3961, 6371
            d_mi, d_km = (R_mi*c) * 200 / 3, (R_km*c) * 200 / 3
            d_mi, d_km = round(d_mi, 2), round(d_km, 2)

            dists.append((d_mi, d_km))

        cities['distance'] = dists
        return pd.Series(dists)

    return calculate_distance_haversine

def convert_str_to_gp(s):
    """Converts the string representation of geopoint S into
    two floats corresponding to latitude and longitude.
    """

    return [radians(float(p.replace('(', '').replace(')', ''))) for p in s.split(',')]