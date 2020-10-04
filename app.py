import flask
from flask import request
from werkzeug.routing import BaseConverter

from AutoCorrect import *
from ArticleScraper import *
from NearbyCities import *
from TwitterScraper import *
from Map import *

class FloatListConverter(BaseConverter):
  """Match floats separated with ';'."""

  # At least one float, separated by ;, with optional trailing ;
  regex = r'-?\d+\.\d+(?:;-?\d+\.\d+)*;?'

  # This is used to parse the url and pass the list to the view function
  def to_python(self, value):
      return [float(x) for x in value.split(';')]

  # This is used when building a url with url_for
  def to_url(self, value):
      return ';'.join(str(x) for x in value)


app = flask.Flask(__name__)
app.url_map.converters['float_list'] = FloatListConverter
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''
    <style>
    h1 {
        font-size: 75px
    }

    h3 {
        font-size: 20px
    }

    h1, h3 {
        text-align: center;
    }

    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>

    <h1>FIRE TALK</h1>
    <h3><i>An on-the-ground live feed of updates to keep you prepared for the worst!</i></h3>

    <br><br>

    <table>
        <tr>
            <th>Call</th>
            <th>Description</th>
            <th>Syntax</th>
            <th>Return Type</th>
        </tr>
        <tr>
            <td>/api/info</td>
            <td>Returns n news sources based on a central city (complete with title, description, and url).</td>
            <td>/api/info?city={{city}}&n={{n}}</td>
            <td>Dictionary/Hash Table</td>
        </tr>
        <tr>
            <td>/api/nearCities</td>
            <td>Returns the nearest n cities, their coordinates, and their AQIs based on a central city.</td>
            <td>/api/nearCities?city={{city}}&n={{n}}</td>
            <td>Dictionary/Hash Table<br>*contains (mi, km), (lat, lon), and (AQI, level)*</td>
        </tr>
        <tr>
            <td>/api/tweets</td>
            <td>Returns the n most recent tweets regarding fires near a specified city.</td>
            <td>/api/tweets?city={{city}}&n={{n}}</td>
            <td>Dictionary/Hash Table</td>
        </tr>
        <tr>
            <td>/api/map</td>
            <td>Returns a Google Map based on a central city and nearby coordinates.</td>
            <td>/api/map/{{city}}/{{geopoints}}<br>*{{geopoints}} = lat1;lon1;lat2;lon2;...*</td>
            <td>HTML</td>
        </tr>
    </table>
    '''


# Basic formatting (REPETITION ISSUE. FIX SOMETIME SOON)
cities = pd.read_csv('worldcities.csv', sep=',')
cities_list = list(cities['city'])

@app.route('/api/info', methods=['GET'])
def get_info():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    info = {}
    urls = [url for url in articleURL(city, n)]

    for i, url in enumerate(urls):
        title = findTitle(url)
        paragraph = paragraphFinder(url)
        
        info[i] = {'title': title, 'paragraph': paragraph, 'url': url}

    return info


@app.route('/api/nearCities', methods=['GET'])
def get_nearby_cities():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    return nearby_cities(city, n)


@app.route('/api/tweets', methods=['GET'])
def tweet_info():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    return scrape_tweets(city, n)


@app.route('/api/map/<city>/<float_list:geopoints>', methods=['GET'])
def display_map(geopoints, city):
    """
    <float_list:geopoints> --> /api/map/37.726;-121.444;37.774;-121.5452;37.809;-121.313
    *Each float is separated by a ;*
    """
    city = auto_correct(cities_list, city)
    return generate_map(geopoints, city)


if __name__ == "__main__":
    app.run()
