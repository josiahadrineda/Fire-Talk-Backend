import requests
import cloudscraper
from requests.exceptions import ReadTimeout
from bs4 import BeautifulSoup, SoupStrainer
from concurrent.futures import ThreadPoolExecutor, as_completed

import app
from GoogleScrapy import *

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

scraper = cloudscraper.create_scraper()

# For urls
reformat = lambda u: u.strip().replace('\r', '').replace('\n', '')

def find_info(city, n):
    """Returns N articles (url, title, paragraph) regarding fires at or near CITY.
    """

    info = {}

    urls, all_urls = find_urls(city, n)

    for i, url in enumerate(urls):
        title = find_title(url)
        paragraph = find_paragraph(url)
        
        info[i] = {'title': title, 'paragraph': paragraph, 'url': url}

    return info, all_urls

def find_more_info(rest, n):
    """Returns N more articles (url, title, paragraph) regarding fires at or near CITY.
    """

    try:
        info = {}

        all_urls = rest
        
        urls = []
        i = 0
        while i < len(all_urls) and len(urls) < n:
            url = find_redir_urls([all_urls[i]])
            if url:
                urls += url
            i += 1
        all_urls = all_urls[i:]

        for i, url in enumerate(urls):
            url = url.replace("['", "").replace("']", "")
            title = find_title(url)
            paragraph = find_paragraph(url)
            
            info[i] = {'title': title, 'paragraph': paragraph, 'url': url}

        return info, all_urls
    except:
        return {}, 'Too many urls requested! Please try again.'

# Uses Scrapy (GoogleScrapy.py)
def find_urls(city, n, limit=15):
    """Returns N urls regarding fires at or near CITY.
    """

    urls = [link['link'].replace("['", "").replace("']", "") for link in scrape_articles(city)[:limit]]
    urls = [reformat(url) for url in urls]

    first_n, rest = urls[:n], urls[n:]

    return find_redir_urls(first_n), rest

def find_redir_urls(urls):
    try:
        return [str(requests.get(reformat(url), timeout=3).url) for url in urls]
    except ReadTimeout:
        return 0

# Uses bs4
def find_title(url):
    """Returns the title of a specified URL.
    """

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

# Uses bs4
def find_paragraph(url):
    """Returns a short to mid-sized paragraph (description) of a specified URL.
    """

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