# KDSP_Twitter_Data_Analysis
# In Project 5 "Twitter Data Analysis", data from Twitter need to be fetched from a specific event, e.g. #football.
# 1. Derive the sentiment of each tweet using Python module
# 2. Top 10 hashtags and users based on their number of tweets in the data set
# 3. Get the followers of a given twitter user from your acquired data set
# 4. Given a twitter user, obtain the tweets and profiles of all followers of the user and show it.

import yaml
import tweepy

# load the credential data from yaml file
def process_yaml(credentials):
    with open(credentials) as c:
        return yaml.safe_load(c)

# extract consumer key and secret
def create_keys(access_data):
    return access_data["twitter_api"]["consumer_key"], access_data["twitter_api"]["consumer_secret"]

# get access to the Twitter API
def twitter_auth(consumer_key, consumer_secret):
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    return api

# test function
def test(api):
    screen_name = 'HaueMariu'
    for follower in tweepy.Cursor(api.followers, screen_name).items(10):
        print(follower.screen_name)


def main():
    access_data = process_yaml("credentials.yaml")
    consumer_key, consumer_secret = create_keys(access_data)
    api = twitter_auth(consumer_key, consumer_secret)

    test(api)


# only execute when run as the main program
if __name__ == "__main__":
    main()
