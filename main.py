# KDSP_Twitter_Data_Analysis
# In Project 5 "Twitter Data Analysis", data from Twitter need to be fetched from a specific event, e.g. #football.
# 1. Derive the sentiment of each tweet using Python module
# 2. Top 10 hashtags and users based on their number of tweets in the data set
# 3. Get the followers of a given twitter user from your acquired data set
# 4. Given a twitter user, obtain the tweets and profiles of all followers of the user and show it.

import yaml
import tweepy
import pandas as pd
import nltk
import re
from textblob import TextBlob
import json
import numpy as np


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


# access required data for a specific event e.g. #football
def twitter_search(api, search):
    search_results = api.search(q=search, lang='en', count='100', tweet_mode='extended', wait_on_rate_limit='True')
    return search_results


# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove @mentions
    text = re.sub(r'#', '', text)  # Remonving the '#' symbol
    text = re.sub(r'RT[\s]\+', '', text)  # Removing RT TODO: RT's are not removed
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyper link

    return text


# Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Create a function to compute the negative, neutral and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# test function
def test(api, data):
    screen_name = 'de'
    i = 1
    for tweet in data:
        print(tweet.full_text)
        i = i + 1;

def main():
    access_data = process_yaml("credentials.yaml")
    consumer_key, consumer_secret = create_keys(access_data)
    api = twitter_auth(consumer_key, consumer_secret)
    tweets = twitter_search(api, '#')
    df = pd.DataFrame([tweet.full_text for tweet in tweets], columns=['Tweets'])
    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    #df = np.array([tweet.full_text for tweet in tweets], columns=['Tweets'])
    df['Screen_Name'] = np.array([tweet.user.screen_name for tweet in tweets])
    df['Screen_Name'] = np.array([tweet.user.screen_name for tweet in tweets])
    print(df['Screen_Name'].value_counts())
    df = df.sort_values(by=['Screen_Name'])
    print(df)
    #test(api, tweets)


# only execute when run as the main program
if __name__ == "__main__":
    main()
