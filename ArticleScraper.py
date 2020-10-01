from bs4 import BeautifulSoup
import requests
import urllib
import csv
from csv import writer
import time
import random
import cloudscraper


proxies = {
    'http': '87.126.43.160:8080',
    'http': '212.154.58.99:37470',
    'http': '134.122.124.106:3128',
}


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
                x = "https://news.google.com" + item['link']    
                results.append(x)

    new_results = []
    i = 0
    while i < n:
        new_results.append(results[i])
        i += 1

    return new_results[0]

def findTitle(url):
    page = (scraper.get(url,proxies = proxies).text)
    soup = BeautifulSoup(page, 'html.parser')

    links = []
    for link in soup.find_all('title'):
        links.append(str(link.text))

    return str(links[0])




def paragraphFinder(url):
    page = (scraper.get(url,proxies = proxies).text)
    soup = BeautifulSoup(page, 'html.parser')

    links = []
    for link in soup.find_all('p'):
        links.append(str(link.text))

    return max(str(links[2]),str(links[3]), str(links[4]))









