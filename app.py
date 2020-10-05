import flask
from flask import render_template, request
from flask_cors import CORS
from werkzeug.routing import BaseConverter

from AutoCorrect import *
from ArticleScraper import *
from GoogleScrapy import *
from NearbyCities import *
from TwitterScraper import *
from Map import *

# For use in display_map (NOT IN USE YET !!!)
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
app.config["DEBUG"] = True
app.url_map.converters['float_list'] = FloatListConverter

CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/info', methods=['GET'])
def get_info():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    return find_info(city, n)

@app.route('/api/nearCities', methods=['GET'])
def get_nearby_cities():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    return nearby_cities(city, n)

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    city = auto_correct(cities_list, request.args.get('city'))
    n = int(request.args.get('n'))

    return scrape_tweets(city, n)

# NOT IN USE YET !!!
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
