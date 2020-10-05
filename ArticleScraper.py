from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib
import csv
from csv import writer
import time
import random
import cloudscraper

from concurrent.futures import ThreadPoolExecutor, as_completed
from GoogleScrapy import *

scraper = cloudscraper.create_scraper()


# Desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# Mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

# DEPRECATED !!!
"""
# Scrapes google search results
def articleURL(city, n):
    city = ''.join(city.split(' '))
    
    query = str(city) + " fire" 
    URL = f"https://news.google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        only_divs = SoupStrainer('div', attrs={'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})
        soup = BeautifulSoup(resp.text, "lxml", parse_only=only_divs)

        processes = []
        with ThreadPoolExecutor(max_workers=n) as executor:
            i = 0
            for g in soup.children:
                if str(g) == 'html':
                    continue
                if i == n:
                    break

                anchor = g.find('a')
                if anchor:
                    processes.append(executor.submit(find_link, anchor))
                i += 1

        results = []
        for task in as_completed(processes):
            results.append(task.result())

        if results:
            for i in range(len(results)):
                r = requests.get(results[i])
                url = str(r.url).strip().replace('\r', '').replace('\n', '')
                results[i] = url
            return results

    return ''

def find_link(anchor):
    link = anchor['href']
    x = "https://news.google.com" + link
    return x"""

def find_articles(city, n):
    urls = [link['link'].replace("['", "").replace("']", "") for link in scrape_articles(city, n)]
    
    reformat = lambda u: str(requests.get(u).url).strip().replace('\r', '').replace('\n', '')
    urls = [reformat(url) for url in urls]

    return urls

def findTitle(url):
    page = (scraper.get(url).text)
    titles = SoupStrainer('title')
    soup = BeautifulSoup(page, 'lxml', parse_only=titles)

    links = []
    for link in soup.children:
        if str(link) == 'html':
            continue

        try:
            words = str(link.text).split(' ')
            if len(words) >= 5:
                return str(link.text).strip()
        except:
            pass

    return ''

def paragraphFinder(url):
    page = (scraper.get(url).text)
    ps = SoupStrainer('p')
    soup = BeautifulSoup(page, 'lxml', parse_only=ps)

    for link in soup.children:
        if str(link) == 'html':
            continue

        try:
            words = str(link.text).split(' ')
            if len(words) >= 15:
                return str(link.text).strip()
        except:
            pass

    return ''