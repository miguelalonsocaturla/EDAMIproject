import tweepy as tw

# your Twitter API key and API secret


consumer_key = 'ACP1iINuWfwzIomeO8kM9ykRw'
consumer_secret = 'gjrB7khX8oQSADDNGQazxTOfIb10IKrIVJcn5jXAgs0cg6TBZt'

# authenticate

client = tw.Client(
    bearer_token="AAAAAAAAAAAAAAAAAAAAADiZXwEAAAAAZAjLMFds6BXXIAdwT7X0KbXCgdA%3DbwQ1Ch2YpilmLE5hbAcOQcvyF6QKiG1uVXjVLIoiGAuxt4VoCS")

# Replace with your own search query
# replace place_country with the code of your country of interest or remove.
query = '#RealMadrid'

# Starting time period YYYY-MM-DDTHH:MM:SSZ (max period back is March 2006)
start_time = '2018-01-01T00:00:00Z'

# Ending time period YYYY-MM-DDTHH:MM:SSZ
end_time = '2018-08-03T00:00:00Z'

# I'm getting the geo location of the tweet as well as the location of the user and setting the number of tweets
# returned to 10 (minimum) - Max is 100

tweets = client.search_recent_tweets(query=query, max_results=10)

# Get list of places and users
hashtags = {p["id"]: p for p in tweets.includes['hashtags']}

tweets_copy = []
# loop through the tweets to get the tweet ID, Date, Text, Author ID, User Location and Tweet Location
for tweet in tweets.data:
    tweets_copy.append(tweet)

print("Total Tweets fetched:", len(tweets_copy))
