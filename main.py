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
from tweepy import TweepError

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
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


# access required data for a specific event e.g. #football
def twitter_search(api, search):
    search_results = api.search(q=search, lang='en', count='100', tweet_mode='extended', wait_on_rate_limit='True')
    return search_results


# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove @mentions
    text = re.sub(r'#', '', text)  # Remonving the '#' symbol
    text = re.sub(r'RT[\s]: ', '', text)  # Removing RT
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

def getHashtags(tweets, event):
    hashtags = []
    for tweet in tweets:
        for word in tweet.lower().split(' '):
            if word.startswith('#'):
                word = re.search('#[a-z0-9]*', word)
                word = word.group(0)
                if word != event.lower():
                    hashtags.append(word)
    return hashtags;

def twitterFollower(api, user, count):
    followers = tweepy.Cursor(api.followers, user).items(count)
    print(followers.next())
    return followers

def getFollowersProfiles(api, followers, count):
    profiles = []
    for follower in followers:
        try:
            line = tweepy.Cursor(api.user_timeline, follower).items(count)
            print("--------------" + str(line.next().user))
            for tweet in line:
                print(tweet.text)
        except TweepError:
            print("Not allowed to access profile!")
        except StopIteration:
            pass

#def convertProfileData(followers, count):


# test function
def test(api, data):
    screen_name = 'de'
    i = 1
    for tweet in data:
        print(tweet.full_text)
        i = i + 1;

def main():
    event = '#DUUUVAL'
    access_data = process_yaml("credentials.yaml")
    consumer_key, consumer_secret = create_keys(access_data)
    api = twitter_auth(consumer_key, consumer_secret)
    tweets = twitter_search(api, event)

    #format output of pandas DataFrame
    #pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    #pd.set_option('display.max_colwidth', 50)
    print(type(tweets))

    df_tweets = pd.DataFrame([tweet.full_text for tweet in tweets], columns=['Tweets'])
    df_tweets['Screen_Name'] = np.array([tweet.user.screen_name for tweet in tweets])

    df_tweets['Tweets_Sentiment'] = df_tweets['Tweets'].apply(cleanTxt)

    #df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df_tweets['Polarity'] = df_tweets['Tweets_Sentiment'].apply(getPolarity)
    df_tweets['Analysis'] = df_tweets['Polarity'].apply(getAnalysis)

    print(df_tweets)

    print(df_tweets['Screen_Name'].value_counts().nlargest(10))

    df_hashtags = pd.DataFrame(getHashtags(df_tweets['Tweets'], event), columns=['Hashtags'])

    print(df_hashtags['Hashtags'].value_counts().nlargest(10))
    count = 11
    followers = twitterFollower(api, 'Jaguars', count)
    df_follower = pd.DataFrame([follower.screen_name for follower in followers], columns=['Follower'])
    print(df_follower)

    followers_Profiles = getFollowersProfiles(api, df_follower['Follower'], count)

    df_follower['location'] = np.array([profile.user.follower for profile in followers_Profiles])



    #test(api, tweets)


# only execute when run as the main program
if __name__ == "__main__":
    main()
