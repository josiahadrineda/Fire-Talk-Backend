"""Distance formula may have some degree of error with regards to actual
distance in mi and km, however, the nearest cities should still be accurate!!!
Also note that many minor cities might not be included within the csv."""

# *There might be a query limit for Nominatim...so BEWARE!*
from geopy.geocoders import Nominatim
# *Requires pandas 1.1.0 or higher*
import pandas as pd

# Basic formatting
cities = pd.read_csv('worldcities.csv', sep=',')

def nearby_cities(city, k=5):
    """Given the name of a CITY and a positive integer K, returns
    the CITY and the nearest K cities as a list of tuples. The format
    of each tuple is (name, (distance in mi, distance in km)).

    *Note: The list is of size K+1, the first element being CITY
    and the rest of the list being the nearest K cities*

    >>> nearby_cities('Tracy')
    [('Tracy', (0.0, 0.0)), ('Mountain House', (8.12, 13.05)), ('Lathrop', (9.06, 14.57)), ('Manteca', (13.35, 21.47)), ('Discovery Bay', (17.77, 28.58)), ('Ripon', (18.72, 30.11))]
    >>> nearby_cities('Thousand Oaks', k=10)
    [('Thousand Oaks', (0.0, 0.0)), ('Westlake Village', (6.51, 10.47)), ('Camarillo', (9.09, 14.62)), ('Moorpark', (9.44, 15.19)), ('Oak Park', (9.62, 15.48)), ('Agoura Hills', (10.1, 16.25)), ('Simi Valley', (13.18, 21.2)), ('Malibu', (13.7, 22.04)), ('Calabasas', (16.32, 26.25)), ('El Rio', (17.42, 28.02)), ('Santa Paula', (17.98, 28.92))]
    >>> nearby_cities('New Yark')
    'You misspelled your city, you MONKEY! Try again.'
    """
    assert k > 0, 'K must be a positive integer.'
    global cities

    try:
        # Check whether CITY exists in cities.csv
        if city not in list(cities['city']):
            return 'You misspelled your city, you MONKEY! Try again.'

        # Determine the coordinates of CITY
        geolocator = Nominatim(user_agent="Fire Watch")
        location = geolocator.geocode(city)
        lat, long = location.latitude, location.longitude

        # Sort city.csv by distance from CITY
        cities = cities.sort_values('geopoint', key=distance(lat, long))
        
        # CITY is most likely to be in nearby_cities
        nearby_cities = cities.head(k+1)
        nearby_cities_list = list(nearby_cities['city'])
        nearby_cities_dists_list = list(zip(nearby_cities['city'], nearby_cities['distance']))
        if city in nearby_cities_list:
            c = nearby_cities_dists_list.pop(nearby_cities_list.index(city))
            nearby_cities_dists_list.insert(0, (city, (0.0, 0.0)))
        else:
            nearby_cities_dists_list.pop()
            nearby_cities_dists_list.insert(0, (city, (0.0, 0.0)))
        return nearby_cities_dists_list
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
            lat2, long2 = [float(p.replace('(', '').replace(')', '')) for p in gp.split(',')]
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
            lat2, long2 = [radians(float(p.replace('(', '').replace(')', ''))) for p in gp.split(',')]
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