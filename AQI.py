import requests
from random import shuffle
from AutoCorrect import *

with open('aqikey.txt') as f:
    contents = f.readlines()
keys = [line.strip().replace('\n', '') for line in contents]

def get_aqi(city, state, country):
    """Gets the AQI and level of health concern for a specified
    CITY, STATE, and COUNTRY.
    """
    inds = list(range(len(keys)))

    # Fix formatting issue
    if country == 'United States':
        country = 'USA'
    else:
        available_countries = ['Afghanistan', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Bahamas', 'Bahrain', 'Bangladesh', 'Belgium', 'Bosnia Herzegovina', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Ecuador', 'Ethiopia', 'Finland', 'France', 'Germany', 'Ghana', 'Guatemala', 'Hong Kong SAR', 'Hungary', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Japan', 'Jordan', 'Kazakhstan', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lithuania', 'Luxembourg', 'Macao SAR', 'Malaysia', 'Malta', 'Mexico', 'Mongolia', 'Myanmar', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Thailand', 'Turkey', 'U.S. Virgin Islands', 'USA', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uzbekistan', 'Vietnam', 'Yemen']
        country = auto_correct(available_countries, country)
    
    # Want to minimize API calls
    if country == 'USA':
        available_states_US = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'Washington, D.C.', 'West Virginia', 'Wisconsin', 'Wyoming']
        state = auto_correct(available_states_US, state)
    else:
        shuffle(inds)
        get_states = input_country(country)

        available_states = keep_trying(0, inds, get_states, "state_not_found")
        state = auto_correct(available_states, state)
    
    # Autocorrect city
    shuffle(inds)
    get_cities = input_state_country(state, country)

    available_cities = keep_trying(0, inds, get_cities, "city_not_found")
    city = auto_correct(available_cities, city)

    # Aggregation of results
    shuffle(inds)
    get_aqi_helper = input_city_state_country(city, state, country)
    return keep_trying(0, inds, get_aqi_helper, {"AQI": "city_not_found", "Level": "N/A"})

def keep_trying(ind, inds, fn, fail):
    if ind >= len(inds):
        return fail

    try:
        return fn(keys[inds[ind]])
    except:
        return keep_trying(ind+1, inds, fn, fail)

def input_country(country):
    def get_states(key):
        url = f'http://api.airvisual.com/v2/states?country={country}&key={key}'
        response = requests.request("GET", url)

        states = response.json()["data"]

        reformatted_states = []
        for state in states:
            reformatted_states.append(state["state"])
        return reformatted_states
    return get_states

def input_state_country(state, country):
    def get_cities(key):
        url = f'http://api.airvisual.com/v2/cities?state={state}&country={country}&key={key}'
        response = requests.request("GET", url)

        cities = response.json()["data"]

        reformatted_cities = []
        for city in cities:
            reformatted_cities.append(city["city"])
        return reformatted_cities
    return get_cities

def input_city_state_country(city, state, country):
    def get_aqi_helper(key):
        url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={key}"
        response = requests.request("GET", url)

        aqi = response.json()["data"]["current"]["pollution"]["aqius"]
        level = rank_aqi(aqi)
        return {"AQI": aqi, "Level": level}
    return get_aqi_helper

def rank_aqi(aqi):
    """Ranks the specified AQI in terms of health concern.
    """

    ranks = [
        "Good",
        "Moderate",
        "Unhealthy for Sensitive Groups",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous"]

    if aqi > 300:
        return ranks[-1]
    aqi = min(max(aqi // 50 - 1, 0) if aqi % 50 == 0 else aqi // 50, 4)
    return ranks[aqi]