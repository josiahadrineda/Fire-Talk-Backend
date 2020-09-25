import flask
from flask import request 
from bs4 import BeautifulSoup
import requests
import urllib
import csv
from csv import writer
import time
import random

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
def article_scraper():  #n is the number of articles to display
    # potentially need to update scraper to use google filtered by time instead of news
    
    city = request.args.get('city')
    n = request.args.get('n')

    n = int(n)



    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"


    query = str(city) + " fire" 
    URL = f"https://news.google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                    }
                x = "news.google.com" + item['link']    
                results.append(x)
    new_results = []
    i=0
    while i < n:
        new_results.append(results[i])
        i+=1
    return new_results[0]


@app.route('/api/nearCities', methods=['GET'])
def get_nearby_cities():
    city = request.args.get('city')
    k = request.args.get('k')
    return nearby_cities(city, k)

app.run()
