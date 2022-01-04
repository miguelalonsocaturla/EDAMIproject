
import tweepy as tw
# your Twitter API key and API secret
consumer_key = 'datBeJPQCuKdWhHTP5ra52Ml6'
consumer_secret = 'BcSS4Bq6FotENZdytJhMpYVl89GFxkn1oCLSjxGK44jEUOzh0e'
access_token = 'HYTHTYH65TYhtfhfgkt34'
access_token_secret = 'ged5654tHFG'
# authenticate
auth = tw.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

search_query = "#RealMadrid -filter:retweets"

# get tweets from the API
#tweets = tw.Cursor(api.search_tweets, q=search_query, lang="es").items(5000)
tweets = tw.Client.search_recent_tweets(search_query)
# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(tweet)

print("Total Tweets fetched:", len(tweets_copy))


