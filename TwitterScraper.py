"""DEPRECATED !!!"""

import tweepy as tw
from flask import jsonify

def scrape_tweets(city, n=5):
    """Returns the most recent N tweets regarding #fire in CITY.
    """

    keys = []
    with open('twitterkeys.txt', 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            keys.append(line)
    cons, cons_secret, acc, acc_secret = keys

    auth = tw.OAuthHandler(cons, cons_secret)
    auth.set_access_token(acc, acc_secret)
    api = tw.API(auth, wait_on_rate_limit=True, parser=tw.parsers.JSONParser())

    city = '+'.join(city.split(' '))
    filt = '-filter:retweets'
    include = ['fire', 'wildfire', 'burning']
    exclude = ['mixtape', 'track', 'song', 'beat', 'remix']

    query = city + ' ' + ' OR '.join(include) + ' -' + ' -'.join(exclude) + ' ' + filt

    tweets = api.search(
        q=query,
        count=n,
        lang='en',
        tweet_mode='extended'
    )

    tweet_dict = {}
    for ind, tweet in enumerate(tweets['statuses']):
        user = tweet['user']['screen_name']
        text = tweet['full_text']
        id_str = tweet['id_str']
        src = f'https://twitter.com/{user}/status/{id_str}'

        tweet_dict[ind] = {'user': user, 'text': text, 'src': src}
    return tweet_dict