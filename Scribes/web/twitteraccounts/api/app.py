import asyncio
from datetime import datetime
from factom import Factomd, FactomWalletd, exceptions
import faust
import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer
import os
import pandas as pd
import time
import tweepy
from typing import List 

from credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from utils import filterTweets, getAllTweets, factomizeTweets, reconstructTweet, sendTweets, getTwitterCredentials
from asyncfxns import tweetFetcher

app = faust.App('Scribes_faust',  broker='kafka://localhost:9092')


# class TwitterAccount(faust.Record):
#     handle: str
#     twitterid: str
#     chainid: str

source_topic = app.topic('Scribes-faust', value_serializer='json')
# base_topic= app.topic('TwitterAccounts', value_serializer= 'json')


@app.agent(source_topic)
async def process(stream):
    async for payload in stream:
        print('TESTING NOW!')
        twitteraccount = json.loads(payload)
        print(twitteraccount['fields'])
        t_account = twitteraccount['fields']
        # Twitter_Account = TwitterAccount(t_account['handle'], t_account['twitterid'], t_account['chainid'])
        # print(Twitter_Account)
        kafka = KafkaClient("localhost:9092")
        producer = SimpleProducer(kafka, value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        producer.send_messages('TwitterAccounts', json.dumps(t_account).encode('utf-8'))



# @app.agent(base_topic)
# async def getAccounts(base_topic):
#     async for account in base_topic:
#         print(account)
#         t_account_topic = account['handle']
#         kafka = KafkaClient("localhost:9092") #initializes kafka client
#         producer = SimpleProducer(kafka, value_serializer=('utf-8')) #initializes kafka producer
#         producer.send_messages('IndividualAccounts', t_account_topic.encode('utf-8'))
#         account_topic = app.topic(str(t_account_topic), value_serializer='json')
#         account_topic.stream()
#         print('New Stream Made')

#         topic = account['handle']
#         chain_id = str(account['chainid'])
#         twitter_id = str(account['twitterid'])

#         Stream_Listener = StreamListener() #Turns Stream Listener Class On
#         Stream_Listener.field_load(twitter_id, chain_id, topic)

#         try:
#             api = getTwitterCredentials(TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET) #authorize api credentials
#             stream = tweepy.Stream(auth = api.auth, listener=Stream_Listener, aync=True) #create a stream for the account
#             stream.filter(follow = [str(twitter_id)], is_async=True) #listens to twitter account and triggers for only the account's tweets
        
#         except Exception as ex: #error handling to restart streamer in the event of it stopping for things like Rate Limit Error
#             print ("[STREAM] Stream stopped! Reconnecting to twitter stream")
#             print (ex)
#             stream.filter(follow = [str(twitter_id)])

#         new_file = tweetFetcher(topic) #creates a csv file of the accounts most recent tweets and filters it
#         cwd = os.getcwd()
#         for file in os.listdir(cwd): 
#             if file.startswith(topic):
#                 sendTweets(file, str(topic)) #writes tweets to factom the csv
#         print('Done')
#         print('waiting to Factomize')
#         consumer = KafkaConsumer(str(topic), 
#                             auto_offset_reset='earliest',
#                             bootstrap_servers=['localhost:9092'],
#                             consumer_timeout_ms=1000)

#         for message in consumer:
#             raw_tweetid = message.value
#             tweetid = raw_tweetid.decode("utf-8") 
#             print(str(tweetid))
#             print(chain_id)
#             factomizeTweets((tweetid),(chain_id)) #Write tweet to Factom
#             print(str(tweetid) + ' Success!')
#             time.sleep(10)

#             consumer.close()
async def start_worker(worker: faust.Worker) -> None:
    """
    :param worker: A Faust worker instance that runs a certain app configuration. This
    consumes and partitions kafka queues based on specific topics
    :return: None
    """
    await worker.start()
if __name__ == '__main__':
    worker = faust.Worker(app, loglevel='info')