import pandas as pd
import requests
import json
import os

bt = os.environ['BEARER_TOKEN']
banned_word_list = list(pd.read_csv('Terms-to-Block.csv').iloc[:, 0])

MONTHS = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
]

def scrape_tweets(city, n):
    """Aggregation of below helpers.
    """

    return main(city, n)

def main(city, n):
    """Performs all the grunt work of the Twitter Scraper.
    """

    bearer_token = auth()
    url = create_url(city, n)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json.dumps(reformat(json_response), indent=4, sort_keys=True)

def auth():
    """Returns the Twitter Developer Bearer Token.
    """

    return bt

def create_url(city, n):
    """Generates N urls based on a query for a specified CITY.
    """

    city = '+'.join(city.split(' '))
    filt = '-is:retweet'
    include = [city + ' ' + word for word in ['fire', 'wildfire', 'burning']]
    exclude = ['mixtape', 'track', 'song', 'beat', 'remix', 'drip'] + banned_word_list
    query = ' OR '.join(include) + ' -' + ' -'.join(exclude) + ' ' + filt

    max_results = f"max_results={n}"
    tweet = "tweet.fields=author_id,id,created_at"
    expansions = "expansions=author_id"
    user = "user.fields=username,name,profile_image_url"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}&{}".format(
        query, max_results, tweet, expansions, user
    )
    return url

def create_headers(bearer_token):
    """Generates header for a Twitter Developer Bearer Token.
    """

    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    """Request bridge (tbh I'm not exactly sure what this does).
    """

    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def reformat(info):
    """Molds the generated tweet info into the desirable format for the API.
    """

    users = [u["username"] for u in info["includes"]["users"]]
    names = [u["name"] for u in info["includes"]["users"]]
    pics = [u["profile_image_url"] for u in info["includes"]["users"]]
    dates = [reformat_date(u["created_at"]) for u in info["data"]]
    texts = [t["text"] for t in info["data"]]
    tweet_ids = [t["id"] for t in info["data"]]
    srcs = [f"twitter.com/{user}/status/{t_id}" for user, t_id in zip(users, tweet_ids)]

    tweet_info = {}
    for ind, (user, name, pic, date, text, id, src) in enumerate(zip(users, names, pics, dates, texts, tweet_ids, srcs)):
        tweet_info[ind] = {"user": user, "name": name, "pic": pic, "date": date, "text": text, "id": id, "src": src}
    return tweet_info

def reformat_date(date):
    """Reformats a DATE given by the Twitter API v2.
    """

    year, month, day = date[:4], date[5:7], date[8:10]
    
    if month[0] == '0':
        month = month[1:]
    if day[0] == '0':
        day = day[1:]
    month = MONTHS[int(month) - 1]
    
    return ' '.join([day, month, year])