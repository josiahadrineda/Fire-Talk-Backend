# *There might be a query limit for Nominatim...so BEWARE!*
from geopy.geocoders import Nominatim
# *Requires pandas 1.1.0 or higher*
import pandas as pd

from math import sqrt

def nearby_cities(city, k=5):
    """Given the name of a CITY and a positive integer K, returns
    the CITY and the nearest K cities as a list.

    *Note: The list is of size K+1, the first element being CITY
    and the rest of the list being the nearest K cities*

    >>> nearby_cities('Tracy')
    ['Tracy', 'Manteca', 'French Camp', 'Vernalis', 'Lyoth', 'Banta']
    >>> nearby_cities('Thousand Oaks', k=10)
    ['Thousand Oaks', 'Newbury Park', 'Camarillo', 'Moorpark', 'Somis', 'Point Mugu Nawc', 'Brandeis', 'Malibu', 'Port Hueneme', 'Oxnard', 'Santa Paula']
    >>> nearby_cities('New Yark')
    'You misspelled your city, you MONKEY! Try again.'
    """
    assert k > 0, 'K must be a positive integer.'

    try:
        # Basic formatting
        cities = pd.read_csv('cities.csv', sep=';')
        cities = cities.drop_duplicates(subset='City', keep='first')
        
        # Check whether CITY exists in cities.csv
        if city not in list(cities['City']):
            return 'You misspelled your city, you MONKEY! Try again.'

        # Determine the coordinates of CITY
        geolocator = Nominatim(user_agent="Fire Watch")
        location = geolocator.geocode(city)
        lat, long = location.latitude, location.longitude

        # Sort city.csv by distance from CITY
        cities['Coordinates'] = list(zip(cities['Latitude'], cities['Longitude']))
        cities = cities.sort_values('Coordinates', key=distance(lat, long))
        
        # CITY is most likely to be in nearby_cities
        nearby_cities = cities.head(k+1)
        nearby_cities_list = list(nearby_cities['City'])
        if city in nearby_cities_list:
            c = nearby_cities_list.pop(nearby_cities_list.index(city))
            nearby_cities_list.insert(0, c)
        else:
            nearby_cities_list.pop()
            nearby_cities_list.insert(0, city)
        return nearby_cities_list
    except AttributeError:
        return 'An error occurred, you MONKEY! Try again.'

def distance(lat, long):
    """Takes the reference latitude LAT and longitude LONG and
    returns a calculate_distance function used to sort cities.csv.
    """

    def calculate_distance(coords):
        dists = []
        for coord in coords:
            lat2, long2 = coord
            x = abs(lat - lat2)
            y = abs(long - long2)
            dist = sqrt(x**2 + y**2)
            dists.append(dist)
        return pd.Series(dists)
    return calculate_distance