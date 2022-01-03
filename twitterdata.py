
import tweepy as tw
# your Twitter API key and API secret

consumer_key = '00uoWhWMhHFv3VvLmRS92wGss'
consumer_secret = 'rSsAQhOO2SZ6QNDXS1D6gIkrzuAD4OJ545xnqDlnM6KhVIR7Uj'
access_token = '1477363091646132228-f3eIclo5ERWkZ0hC7ldO5ISncMmMBR'
access_token_secret = 'rqvmXTHyQHLprD17WzUDIHjTbQrWVuDV8d73JnY4xJUVg'
# authenticate
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_query = "#RealMadridFutbolClub -filter:retweets"

# get tweets from the API
tweets = tw.Cursor(api.search_tweets, q=search_query, lang="es").items(5000)
# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(api.get_status(id=tweet.id, tweet_mode='extended').full_text)

print("Total Tweets fetched:", len(tweets_copy))


