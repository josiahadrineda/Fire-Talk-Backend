import tweepy as tw

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
    api = tw.API(auth, wait_on_rate_limit=True)

    city = '+'.join(city.split(' '))
    filt = ' -filter:retweets'
    tweets = tw.Cursor(
        api.search,
        q=[city+filt, 'fire'+filt],
        lang='en'
    ).items(n)

    recent_tweets = []
    for tweet in tweets:
        recent_tweets.append(tweet.text)

    for tweet in set(recent_tweets):
        if recent_tweets.count(tweet) > 1:
            i = recent_tweets.index(tweet) + 1
            while i < len(recent_tweets):
                if recent_tweets[i] == tweet:
                    recent_tweets.pop(0)
                else:
                    i += 1

    return {i: recent_tweets[i] for i in range(len(recent_tweets))} if recent_tweets else ''