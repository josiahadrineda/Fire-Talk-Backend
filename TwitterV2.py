import requests
import json

with open('BearerToken.txt', 'r') as f:
    bt = f.readline()

def auth():
    return bt

def create_url(city, n):
    query = f"{city} fire -is:retweet"
    expansions = "expansions=author_id"
    tweet = "tweet.fields=author_id,id"
    user = "user.fields=username"
    max_results = f"max_results={n}"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query, max_results, expansions, tweet, user
    )
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def reformat(info):
    users= [t["text"] for t in info["data"]]
    texts = [u["username"] for u in info["includes"]["users"]]
    tweet_ids = [t["id"] for t in info["data"]]
    srcs = [f"twitter.com/{user}/status/{t_id}" for user, t_id in zip(users, tweet_ids)]

    tweet_info = {}
    for ind, (user, text, src) in enumerate(zip(users, texts, srcs)):
        tweet_info[ind] = {"user": user, "text": text, "src": src}
    return tweet_info

def main(city, n):
    bearer_token = auth()
    url = create_url(city, n)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json.dumps(reformat(json_response), indent=4, sort_keys=True)

def scrape_tweets(city, n):
    return main(city, n)