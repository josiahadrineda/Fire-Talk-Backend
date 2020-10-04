"""Distance formula may have some degree of error with regards to actual
distance in mi and km, however, the nearest cities should still be accurate!!!
Also note that many minor cities might not be included within the csv."""

# *There might be a query limit for Nominatim...so BEWARE!*
from geopy.geocoders import Nominatim
from collections import OrderedDict
# *Requires pandas 1.1.0 or higher*
import pandas as pd

from AQI import *

# Basic formatting
cities = pd.read_csv('worldcities.csv', sep=',')

def nearby_cities(city, k=5):
    """Given the name of a CITY and a positive integer K, returns
    the CITY and the nearest K cities as a list of tuples. The format
    of each tuple is (name, (distance in mi, distance in km)).

    *Note: The list is of size K+1, the first element being CITY
    and the rest of the list being the nearest K cities*

    *Update: Also returns AQI for CITY*
    *Update: Also returns geopoint and city data for Map.py*
    """
    assert k > 0, 'K must be a positive integer.'
    
    global cities

    try:
        # Determine the coordinates of CITY
        geolocator = Nominatim(user_agent="Fire Watch")
        location = geolocator.geocode(city)
        lat, long = location.latitude, location.longitude

        # Sort city.csv by distance from CITY
        cities = cities.sort_values('geopoint', key=distance(lat, long))
        
        # CITY is most likely to be in nearby_cities
        nearby_cities = cities.head(k+1)
        
        nearby_cities_states = list(nearby_cities['admin_name'])
        nearby_cities_countries = list(nearby_cities['country'])

        nearby_cities_geos = list(nearby_cities['geopoint'])
        nearby_cities_list = list(nearby_cities['city'])
        nearby_cities_dists_list = list(zip(nearby_cities['city'], nearby_cities['distance']))
        if city in nearby_cities_list:
            c = nearby_cities_dists_list.pop(nearby_cities_list.index(city))
        else:
            nearby_cities_dists_list.pop()
        nearby_cities_dists_list.insert(0, (city, (0.0, 0.0)))

        for i in range(len(nearby_cities_dists_list)):
            ci, st, co = nearby_cities_list[i], nearby_cities_states[i], nearby_cities_countries[i]
            _, dist = nearby_cities_dists_list[i]
            nearby_cities_dists_list[i] = (ci, (get_aqi(ci, st, co), dist))
        
        od = OrderedDict()
        od['geos'] = nearby_cities_geos
        od['dists'] = nearby_cities_dists_list
        return od
    except AttributeError:
        return 'An error occurred, you MONKEY! Try again.'


from math import sqrt, sin, cos, atan2, radians

def distance(lat, long):
    """Takes the reference latitude LAT and longitude LONG and
    returns a calculate_distance function used to sort cities.csv.
    """
    global cities

    # Should only be used if Haversine goes wrong
    """def calculate_distance(geopoint):
        dists = []
        for gp in geopoint:
            lat2, long2 = convert_str_to_gp(gp)
            y = lat2 - lat
            x = long2 - long
            dist = sqrt(x**2 + y**2)
            dists.append(dist)
        cities['distance'] = dists
        return pd.Series(dists)"""

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