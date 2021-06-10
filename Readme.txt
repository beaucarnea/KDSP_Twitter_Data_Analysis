KDSP - Twitter Data Analysis
Name: Marius Hauenstein
Matriculation Number: 3178081

--------------------------------
$ Project description

In Project 5 "Twitter Data Analysis", data from Twitter need to be fetched from a specific event, e.g. #football.
1. Derive the sentiment of each tweet using Python module
2. Top 10 hashtags and users based on their number of tweets in the data set
3. Get the followers of a given twitter user from your acquired data set
4. Given a twitter user, obtain the tweets and profiles of all followers of the user and show it.

--------------------------------
$ environment
Project was developed in Pycharm with a jupyter notebook.

--------------------------------
$ API Configuration

To get started you need an Twitter developer account.
Create a project and app in the account.
Inside of an App in a Project you can view, create, regenerate, or revoke the consumer key and consumer secret.

Replace the "XXXXXXXXXX" in the "credentials.yaml" file with your personal consumer key and consumer secret.

--------------------------------
$ Modules needed for execution:

1. yaml
2. tweepy
3. numpy
4. pandas
5. re
6. textblob
7. matplotlib
8. wordcloud
9. PIL

--------------------------------
$ required variables

In the first code section you can set:
1. "event" - set the "event" variable with your favourite event
    default: "#NFLDraft"
2. "follower_count" - will set the number of followers for the api requests
    default: 10
3. "tweet_count" - will set the number of tweets for the api requests
    default: 10