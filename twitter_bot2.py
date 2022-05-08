# twitter bot to scrape latest tweets and user-public-info
from re import U
import requests
import os 
import json


bearer_token = os.environ.get("BEARER_TOKEN")
user_agent = os.environ.get("User-Agent")


# Reads the content of a file paticularly JSON file
def read_file(file):
	with open(file, 'r') as f:
		data = json.loads(f.read())
		return data


# Function to save data into a file
def save_to_file(final_result,filename):
	with open(filename, "w+") as f:
		json.dump(final_result, f, indent = 2)


# Fetch the guest token for twitter 
def get_guest_token():
	url = "	https://api.twitter.com/1.1/guest/activate.json"
	Headers = {"Authorization":bearer_token, 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0','content-type':'application/x-www-form-urlencoded'}
	response = requests.post(url, headers=Headers)
	r = response.json()
	token = r['guest_token']
	return token


def check_token_and_get_response(url):
	token = read_file('token.json')
	Headers = {"Authorization":bearer_token,"User-Agent":user_agent,"x-guest-token" : token}
	response = requests.get(url, headers=Headers)
	if response.status_code != 200:
		print("hello")
		token = get_guest_token()
		f = open('token.json', 'r+')
		f.truncate(0) 
		save_to_file(token, 'token.json')
	return response.json()


# Get the user's public data
def get_user_data(username):	
	url = 'https://twitter.com/i/api/graphql/Bhlf1dYJ3bYCKmLfeEQ31A/UserByScreenName?variables={"screen_name":"'+username+'","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}'
	return check_token_and_get_response(url)


# Get user profile filtered data
def get_user_profile_filtered_data(x):
	y = x['data']['user']['result']['legacy']
	filtered_output = {'created at':y['created_at'], "description":y["description"],"followers_count":y["followers_count"],
			 "friends_count":y[ "friends_count"],"location":y["location"],"name":y["name"],}
	return filtered_output


# Get the latest tweets unfiltered data upt 40
def get_tweets():
	url = 'https://twitter.com/i/api/graphql/07VfD4dpV9RcW5dsbCjYuQ/UserTweets?variables={"userId":"1349149096909668363","count":40,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true,"__fs_responsive_web_like_by_author_enabled":false,"__fs_dont_mention_me_view_api_enabled":true,"__fs_interactive_text_enabled":true,"__fs_responsive_web_uc_gql_enabled":false,"__fs_responsive_web_edit_tweet_api_enabled":false}'
	return check_token_and_get_response(url)


# Get the filtered tweet's data
def get_filtered_tweets(x):
	li = []
	y = x['data']['user']['result']["timeline_v2"]["timeline"]['instructions'][1]['entries']
	for i in range(0,40): 
		if 'itemContent' in y[i]["content"].keys():
			z = y[i]["content"]['itemContent']['tweet_results']['result']['legacy']
			filtered_output = {"created_at":z["created_at"],"full_text":z["full_text"], "retweet_count":z["retweet_count"],"reply_count":z["reply_count"],
					"quote_count":z["quote_count"],"favorite_count":z["favorite_count"]}
			li.append(filtered_output)		
	return li


# Function calling and user input
username = input("Enter the usename: ")
user_data = get_user_profile_filtered_data(get_user_data(username))
save_to_file(user_data, 'tweets.json')
