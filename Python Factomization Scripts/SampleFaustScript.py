from datetime import datetime
from factom import Factomd, FactomWalletd, exceptions
import faust
import json
import os
import pandas as pd
import pickle
import time
import tweepy
from typing import List 

from Credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from FunctionLibrary import filterTweets, getAllTweets, factomizeTweets, reconstructTweet, sendTweets, getTwitterCredentials
from TimelineScraperScript import tweetFetcher
from StreamerFxn import StreamListener

# Note, this app was originally designed for local testing purposes. Hence there are hardcoded components. All hardcoded
# components will be removed prior to production.

#twitter auth keys and using them to gain access to api functionality with tweepy
auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET) #Gathers Twitter Keys
auth.set_access_token(TWITTER_APP_KEY, TWITTER_APP_SECRET) #Gathers Twitter APP Keys
api = tweepy.API(auth)

#Name of the faust app
app = faust.App(
    'Scribe-Test',
    broker='kafka://localhost:9092',
)

#topic being consumed by the kafka consumer/faust agent (name of the twitter account being tracked)
tweet_topic = app.topic('fct_bot', value_serializer='json')


class twitterAccount(faust.Record, serializer='json', polymorphic_fields=True):
    handle: str
    twitterid: str
    chainid: str

"""
Below Defines the faust agent. This is what will work in the background to manage to ensure that all task and mesage
queues are consumed/ordered properly and run them in the backgound. In the context of this program, the agent will
subscirbe to the the stream of tweets being generated from the kafka producer in both of these tasks defined below.
It will then take the payload from the stream, in this case a tweetid, and then use that to reconstruct a tweet that
will then be written to the factom blockchain. It then sleeps for 10 seconds to avoid any rate limit errors with 
writing to quickly to the blockchain. This fxn calls the factomizeTweets fuction from the FunctionLibrary.py file. More
documentation on how that works may be found there
"""
@app.agent(tweet_topic)
async def process(stream): #start asynchronous stream process
    async for payload in stream: #process tweetid payloads in stream for a given topic/twitter account
        tweetid = payload
        factomizeTweets(int(tweetid),chain_id='707efd411d49e98c9f10e48a9b1b0ff9f30680e2fb777620ef810b5aabc6d8b7') #Write tweet to Factom
        print(str(tweetid) + ' Success!')
        time.sleep(10)


"""
Below is the first task that will be run by faust when the program is initiated. It will asynchronously start a
tweepy stream listener in the background that will use the twitter id to track a twitter account. Every time that 
account tweets, the stream listener will write the tweet id to a message queue through a kafka producer so that it 
may be reconstructed by the kafka consumer and written to the Factom Blockchain at a later time. This task utilizes 
the tweepy stream Listener class and a custom listener imported from the StreamerScript.py file to perform the work. 
More documentation on how the Function works may be found there.
"""
@app.task()
async def start_streamer():
    print('Daemon Started, Streamer Started!')
    topic = 'fct_bot'
    chain_id = '707efd411d49e98c9f10e48a9b1b0ff9f30680e2fb777620ef810b5aabc6d8b7'
    twitter_id = 1128123860686200832

    Stream_Listener = StreamListener() #Turns Stream Listener Class On
    Stream_Listener.field_load(twitter_id, chain_id, topic)

    try:
        print('Waiting For Tweets...')
        api = getTwitterCredentials(TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET) #authorize api credentials
        stream = tweepy.Stream(auth = api.auth, listener=Stream_Listener, aync=True) #create a stream for the account
        stream.filter(follow = [str(twitter_id)], is_async=True) #listens to twitter account and triggers for only the account's tweets
    
    except Exception as ex: #error handling to restart streamer in the event of it stopping for things like Rate Limit Error
        print ("[STREAM] Stream stopped! Reconnecting to twitter stream")
        print (ex)
        stream.filter(follow = [str(twitter_id)])

"""
This is the second task that the app performs upon starting. Once the streamer is turned on, the application will then
start this task, which is a program to scrape the tracked accounts timeline. It will gather the account's ~3000 most recent
tweets, filter them so that only the account's original tweets remain, and then begin writing them to a kafka stream for the
topic. This task utilizes the tweetFetcher and sendTweets methods defined in the TimelineScraperScript.py and FunctionLibrary.py files respectively.
Further documentation on how these fxns work may be found there.
"""
@app.task()
async def start_scraper():
    print('scraper started!')
    topic = 'fct_bot'
    new_file = tweetFetcher(topic) #creates a csv file of the accounts most recent tweets and filters it
    cwd = os.getcwd()
    for file in os.listdir(cwd): 
        if file.startswith(topic):
            sendTweets(file, str(topic)) #writes tweets to factom the csv
    print('Done')


if __name__ == '__main__':
    app.main()
