from datetime import datetime
from factom import Factomd, FactomWalletd, exceptions
import faust
from faustapp.app import app
import json
import os
import pandas as pd
import time
import tweepy
from typing import List 

from twitteraccounts.api.credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from twitteraccounts.api.asyncfxns import tweetFetcher
from twitteraccounts.api.utils import factomizeTweets, sendTweets

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from twitteraccounts.models import twitterAccount


# Note, this app was originally designed for local testing purposes. Hence there are hardcoded components. All hardcoded
# components will be removed prior to production.

#twitter auth keys and using them to gain access to api functionality with tweepy
auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET) #Gathers Twitter Keys
auth.set_access_token(TWITTER_APP_KEY, TWITTER_APP_SECRET) #Gathers Twitter APP Keys
api = tweepy.API(auth)

#topic being consumed by the kafka consumer/faust agent (name of the twitter account being tracked)

class twitteraccount(faust.Record, serializer='json', polymorphic_fields=True):
    handle: str
    twitterid: str
    chainid: str

@app.agent(tweet_topic)
async def process(stream): #start asynchronous stream process
    async for payload in stream: #process tweetid payloads in stream for a given topic/twitter account
        tweetid = payload
        chainid=twitterAccount.twitteraccount.chainid
        factomizeTweets(int(tweetid),chain_id=chainid) #Write tweet to Factom
        print(str(tweetid) + ' Success!')
        time.sleep(10)

@app.task()
async def start_scraper(tweet_topic):
    topic = tweet_topic
    new_file = tweetFetcher(topic) #creates a csv file of the accounts most recent tweets and filters it
    cwd = os.getcwd()
    for file in os.listdir(cwd): 
        if file.startswith(topic):
            sendTweets(file, str(topic)) #writes tweets to factom the csv
