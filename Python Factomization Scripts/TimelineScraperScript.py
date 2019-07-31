from factom import Factomd, FactomWalletd, exceptions #python Factom API
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

import json
import os
import sys
import tweepy


from Credentials import TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from FuncionLibrary import filterTweets, getAllTweets, sendTweets


#### Consolidates Tweets from an Accounts Timeline into a CSV file that can then be written to Factom
def tweetFetcher(topic):

    topic = topic # topic == twitter handle

    auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET) #Gathers Twitter Keys
    auth.set_access_token(TWITTER_APP_KEY, TWITTER_APP_SECRET) #Gathers Twitter APP Keys
    api = tweepy.API(auth)

    getAllTweets(topic) #fetches up to 3120 most recent tweets from a users timeline & creates a csv file of them

    cwd = os.getcwd()

    for file in os.listdir(cwd):
        if file.endswith('.csv'):
            new_file = filterTweets(file) #filters the csv file so that only tweets from the account being tracked are present i.e no retweets, replies to their tweets, etc.
            os.remove(file)
    return new_file

### If you want to run this file locally, have an apache kafka server running and then from a separate terminal run python ScrapeFxn.py 'twitter handle you want to track"
if __name__ == '__main__':

    topic = sys.argv[1]
    #chain_id = sys.argv[2]

    new_file = tweetFetcher(topic)
    #kafka = KafkaClient("localhost:9092")
    #producer = SimpleProducer(kafka, value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.startswith(topic):
            sendTweets(file, str(topic)) #writes tweets to factom the csv