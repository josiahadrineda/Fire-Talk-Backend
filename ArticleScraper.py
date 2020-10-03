from bs4 import BeautifulSoup
import requests
import urllib
import csv
from csv import writer
import time
import random
import cloudscraper


scraper = cloudscraper.create_scraper()


# Desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# Mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

# Scrapes google search results
def articleURL(city, n):
    
    query = str(city) + " fire" 
    URL = f"https://news.google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "lxml")
        results = []
        for g in soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc')[:n]:
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                x = "https://news.google.com" + link 
                results.append(x)

        if results:
            for i in range(len(results)):
                r = requests.get(results[i])
                url = str(r.url).strip().replace('\r', '').replace('\n', '')
                results[i] = url
            return results

    return ''

def findTitle(url):
    page = (scraper.get(url).text)
    soup = BeautifulSoup(page, 'lxml')

    links = []
    for link in soup.find_all('title'):
        try:
            words = str(link.text).split(' ')
            if len(words) >= 5:
                return str(link.text).strip()
        except:
            pass

    return ''

def paragraphFinder(url):
    page = (scraper.get(url).text)
    soup = BeautifulSoup(page, 'lxml')

    for link in soup.find_all('p'):
        try:
            words = str(link.text).split(' ')
            if len(words) >= 15:
                return str(link.text).strip()
        except:
            pass

    return ''