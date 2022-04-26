# twitter bot using requests

import requests
import os
import json

bearer_token = os.environ.get("BEARER_TOKEN")

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def recent_tweets_of_user():
    twitter_user = input("Enter the username")
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': '(from:'+twitter_user+' -is:retweet)','tweet.fields': 'author_id' , 'max_results':15}
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


def tweets_with_keywords_hashtags():
    keywords_a = input("Enter the keyqords: ")
    keywords_b = input("Enter the keyqord 2: ")

    search_url = "https://api.twitter.com/2/tweets/search/recent"

    query_params = {'query':'('+keywords_a+' OR '+keywords_b+') lang:en -birthday -is:retweet'}
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))

tweets_with_keywords_hashtags()    
