import pandas as pd
import requests
import json
import os

bt = os.environ['BEARER_TOKEN']
banned_word_list = list(pd.read_csv('Terms-to-Block.csv').iloc[:, 0])

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

    expansions = "expansions=author_id"
    tweet = "tweet.fields=author_id,id"
    user = "user.fields=username"
    max_results = f"max_results={n}"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query, max_results, expansions, tweet, user
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
    # pics = [u["profile_image_url"] for u in info["includes"]["users"]]
    dates = [u["created_at"] for u in info["data"]]
    texts = [t["text"] for t in info["data"]]
    tweet_ids = [t["id"] for t in info["data"]]
    srcs = [f"twitter.com/{user}/status/{t_id}" for user, t_id in zip(users, tweet_ids)]

    tweet_info = {}
    for ind, (user, name, date, text, id, src) in enumerate(zip(users, names, dates, texts, tweet_ids, srcs)):
        tweet_info[ind] = {"user": user, "name": name, "date": date, "text": text, "id": id, "src": src}
    return tweet_info