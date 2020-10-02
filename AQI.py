"""THIS FUNCTION ONLY APPLIES INSIDE THE STATES"""

import requests

key = open('aqikey.txt').read()

def get_aqi(city, state, country):
    """Gets the AQI and level of health concern for a specified
    CITY, STATE, and COUNTRY.
    """

    if city == "New York":
        city = "New York City"

    try:
        url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={key}"
        response = requests.request("GET", url)

        aqi = response.json()["data"]["current"]["pollution"]["aqius"]
        level = rank_aqi(aqi)
        return {"AQI": aqi, "Level": level}
    except KeyError:
        return {"AQI": "city_not_found", "Level": "N/A"}

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

    aqi = min(aqi, 300)
    aqi = max(aqi // 50 - 1, 0) if aqi % 50 == 0 else aqi // 50
    return ranks[aqi]