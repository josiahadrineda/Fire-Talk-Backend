import requests

key = open('aqikey.txt').read()

def get_aqi(latitude, longitude):
    """Gets the AQI for a specified CITY.
    """

    url = f"http://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={key}"
    response = requests.request("GET", url)

    return {"AQI": response.json()["data"]["current"]["pollution"]["aqius"]}