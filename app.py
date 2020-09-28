import flask
from flask import request 


from ArticleScraper import *
from NearbyCities import *


proxies = {
    'http': '87.126.43.160:8080',
    'http':'212.154.58.99:37470',
    'http':'134.122.124.106:3128',
}


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Monkeys write a code that save California </h1>
<p>We are writing a webscraper that compiles data on local fires</p>'''


@app.route('/api/articles', methods=['GET'])
  # article scraper
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
    k = request.args.get('k')

    return nearby_cities(city, k)

app.run()