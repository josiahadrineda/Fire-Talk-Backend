import flask
from flask import request 
from bs4 import BeautifulSoup
import requests
import urllib
import csv
from csv import writer
import time
import random


from ArticleScraper import *
from NearbyCities import *


proxies = {
    'http': '87.126.43.160:8080',
    'http':'212.154.58.99:37470',
    'http':'134.122.124.106:3128',
}



app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Monkeys write a code that save California </h1>
<p>We are writing a webscraper that compiles data on local fires</p>'''


@app.route('/api/articles', methods=['GET'])    # article scraper
def make_article_scraper():  #n is the number of articles to display
    # potentially need to update scraper to use google filtered by time instead of news
    
    city = request.args.get('city')
    n = int(request.args.get('n'))

    return banana(city, n)


@app.route('/api/nearCities', methods=['GET'])
def get_nearby_cities():
    city = request.args.get('city')
    k = request.args.get('k')

    return nearby_cities(city, k)

if __name__ == "__main__":
    app.run()
