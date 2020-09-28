"""THIS FUNCTION ONLY APPLIES INSIDE THE STATES"""

import requests

key = open('aqikey.txt').read()

def get_aqi(city, state, country):
    """Gets the AQI for a specified CITY, STATE, and COUNTRY.
    """

    if city == "New York":
        city = "New York City"

    try:
        url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={key}"
        response = requests.request("GET", url)

        return {"AQI": response.json()["data"]["current"]["pollution"]["aqius"]}
    except KeyError:
        return {"AQI": "city_not_found"}