"""
To Do:
- Modify output to give distances along with names of cities
- Overall efficiency of program
    - Maybe devise a way to shorten the amount of cities to be sorted for output?
    - Limit k to appx. 20?
"""

# *There might be a query limit for Nominatim...so BEWARE!*
from geopy.geocoders import Nominatim
# *Requires pandas 1.1.0 or higher*
import pandas as pd

# I know that using global variables is a sin but whatever...
g_dists = []

def nearby_cities(city, k=5):
    """Given the name of a CITY and a positive integer K, returns
    the CITY and the nearest K cities as a list of tuples. The format
    of each tuple is (name, distance in mi, distance in km).

    *Note: The list is of size K+1, the first element being CITY
    and the rest of the list being the nearest K cities*

    >>> nearby_cities('Tracy')
    ['Tracy', 'Manteca', 'Vernalis', 'French Camp', 'Lyoth', 'Banta']
    >>> nearby_cities('Thousand Oaks', k=10)
    ['Thousand Oaks', 'Newbury Park', 'Camarillo', 'Moorpark', 'Somis', 'Point Mugu Nawc', 'Brandeis', 'Malibu', 'West Hills', 'Santa Paula', 'Westlake Village']
    >>> nearby_cities('New Yark')
    'You misspelled your city, you MONKEY! Try again.'
    """
    assert k > 0, 'K must be a positive integer.'

    try:
        # Basic formatting
        cities = pd.read_csv('cities.csv', sep=',')
        
        # Check whether CITY exists in cities.csv
        if city not in list(cities['City']):
            return 'You misspelled your city, you MONKEY! Try again.'

        # Determine the coordinates of CITY
        geolocator = Nominatim(user_agent="Fire Watch")
        location = geolocator.geocode(city)
        lat, long = location.latitude, location.longitude

        # Sort city.csv by distance from CITY
        cities = cities.sort_values('geopoint', key=distance(lat, long))
        
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


from math import sqrt, sin, cos, atan2, radians

def distance(lat, long):
    """Takes the reference latitude LAT and longitude LONG and
    returns a calculate_distance function used to sort cities.csv.
    """

    lat, long = radians(lat), radians(long)

    #Haversine Formula
    def calculate_distance(geopoint):
        global g_dists
        dists = []
        for gp in geopoint:
            lat2, long2 = [radians(float(p)) for p in gp.split(',')]
            y = radians(lat2 - lat)
            x = radians(long2 - long)

            a = sin(y/2)**2 + cos(lat) * cos(lat2) * sin(x/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))

            R_mi, R_km = 3961, 6371
            d_mi, d_km = (R_mi*c) * 100, (R_km*c) * 100

            dists.append((d_mi, d_km))
        g_dists = dists.copy()
        return pd.Series(dists)

    return calculate_distance

print(nearby_cities('Tracy'))
print(nearby_cities('Thousand Oaks', k=10))