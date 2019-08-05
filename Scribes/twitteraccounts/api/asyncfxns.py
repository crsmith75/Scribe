from factom import Factomd, FactomWalletd, exceptions #python Factom API
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

import csv
from datetime import datetime
import json
import os
import sys
import time
import tweepy


from twitteraccounts.api.credentials import TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from twitteraccounts.api.utils import filterTweets, getAllTweets, sendTweets, filterTweets, getAllTweets, fromCreator, getKeys, getTwitterCredentials


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

"""
This file defines the stream listern object that is used to track a speciied twitter account and send only tweet ids from his or her
original tweets to a kafka message queue using a kafka producer that can then be consumed at a later time so that they may be used
to write tweets to the factom blockchain. This class uses several functions from the HelperFxns.py file, so if you may find further
documentation on them there.
"""
class StreamListener(tweepy.StreamListener):

    def field_load(self, twitter_id, chain_id, topic):
        self.twitter_id = twitter_id
        self.chain_id = chain_id
        self.topic = topic

        print(self.twitter_id, self.chain_id, self.topic)

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        
        if fromCreator(status): #filters tweets related to an account so only the original tweets trigger a response
            
            print('Tweet Filtered!')
            
            try:

                userid = status.user.id
                user_id = str(userid).replace("'", '"')
                print(str(userid))

                tweetid = str(status.id)
                tweet_id = str(tweetid).replace("'", '"')
                print(tweetid)

                name = status.user.screen_name #pulls username of tweeter
                print('@',name, 'tweeted', status.text) #prints tweet to terminal
                date = datetime.now()
                
                chain_id = str(self.chain_id)
                topic = self.topic
                
                kafka = KafkaClient("localhost:9092")
                producer = SimpleProducer(kafka, value_serializer=('utf-8'))
                
                producer.send_messages((str(topic)), tweet_id.encode('utf-8'))
                print('Sending Tweet to Mempool!')
                print('Received at Mempool!') 
                
            except BaseException as e:
                print("Error on_data %s" % str(e))
                return True
      
        def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream
            print ("Stream restarted")

        def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream
            print ("Stream restarted")
