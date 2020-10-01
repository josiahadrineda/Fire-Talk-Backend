import flask
from flask import request
from werkzeug.routing import BaseConverter

from ArticleScraper import *
from NearbyCities import *
from Map import *

class StringListConverter(BaseConverter):
  """Match strings separated with ';'."""

  # At least one string, separated by ;, with optional trailing ;
  regex = r'.+(?:;.+)*;?'

  # This is used to parse the url and pass the list to the view function
  def to_python(self, value):
      return [str(x) for x in value.split(';')]

  # This is used when building a url with url_for
  def to_url(self, value):
      return ';'.join(str(x) for x in value)

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
app.url_map.converters['str_list'] = StringListConverter
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Monkeys write a code that save California </h1>
    <p>We are writing a webscraper that compiles data on local fires</p>'''


@app.route('/api/articles', methods=['GET'])
def article_info():
    city = request.args.get('city')
    n = int(request.args.get('n'))

    return articleURL(city, n)


@app.route('/api/title', methods=['GET'])
def title_Finder():
    url = request.args.get('url')
    return findTitle(url)


@app.route('/api/nearCities', methods=['GET'])
def get_nearby_cities():
    city = request.args.get('city')
    k = int(request.args.get('k'))

    return nearby_cities(city, k)


@app.route('/api/paragraph', methods=['GET'])
def get_paragraph():
  url = request.args.get('url')
  return paragraphFinder(url)



@app.route('/api/map/<city>/<float_list:geopoints>', methods=['GET'])
def display_map(geopoints, city):
    """
    Example of usage:

    <float_list:geopoints> --> /api/map/37.726;-121.444;37.774;-121.5452;37.809;-121.313
    *Each float is separated by a ;*
    """

    return generate_map(geopoints, city)


if __name__ == "__main__":
    app.run()
