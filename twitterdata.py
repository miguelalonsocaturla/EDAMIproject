from unittest import TestCase

import requests
import json
import re
# its bad practice to place your bearer token directly into the script (this is just done for illustration purposes)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANK6XwEAAAAA6kIAE1i8YVzGmltmuaaHdMUgg9c%3D77qJcNxLM88NAchFp6y2XqDVpzo7xorUyHA2KQBXqHjmWJrlge"


def search_twitter(query, max_results, tweet_fields, bearer_token=BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query=%23RealMadrid&max_results=10&tweet.fields=text"
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


class testtwitter(TestCase):
    # search term
    query = "%23RealMadrid"
    # twitter fields to be returned by api call
    tweet_fields = "tweet.fields=text"
    max_results = 10
    # twitter api call
    json_response = search_twitter(query=query, max_results=max_results, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)
    # pretty printing
    print(json.dumps(json_response).)


    #re.findall(r'\B#\w*[a-zA-Z]+\w*', json.dumps(json_response, indent=4, sort_keys=True))

