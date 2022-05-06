import requests
import os 

bearer_token = os.environ.get("BEARER_TOKEN")
user_agent = os.environ.get("User-Agent")

url = 'https://twitter.com/i/api/graphql/Bhlf1dYJ3bYCKmLfeEQ31A/UserByScreenName?variables={"screen_name":"narendramodi","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}'

Headers = {"Authorization":bearer_token,"User-Agent":user_agent,"x-guest-token" : "1522543129496535041","x-twitter-active-user":"yes","x-twitter-client-language":"en"}

response = requests.get(url, headers=Headers)

print("Status Code", response.status_code)
print("JSON Response ", response.json())