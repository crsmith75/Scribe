import csv
from datetime import datetime
import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer
import sys
import time
import tweepy

from Credentials import EC_ADDRESS, FCT_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from FunctionLibrary import filterTweets, getAllTweets, factomizeTweets, fromCreator, getKeys, getTwitterCredentials
"""
This file defines the stream listern object that is used to track a speciied twitter account and send only tweet ids from his or her
original tweets to a kafka message queue using a kafka producer that can then be consumed at a later time so that they may be used
to write tweets to the factom blockchain. This class uses several functions from the FunctionLibrary.py file, so if you may find further
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


### If you wish to run locally, have an apache kafka server running and in a separate terminal run python StreamerFxn.py 'some_twitter_id' 'some chain_id' 'some_twitter_handle'
if __name__ == '__main__':

    topic = sys.argv[3]
    chain_id = sys.argv[2]
    twitter_id = sys.argv[1]

    print('Turning Streamer On....')
    StreamListener = StreamListener() #Turns Stream Listener Class On
    StreamListener.field_load(twitter_id, chain_id, topic)

    print('Streamer On, Ready to Factomize Some Tweets!')
    
    try:
        print('Waiting For Tweets...')
        api = getTwitterCredentials(TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET)
        stream = tweepy.Stream(auth = api.auth, listener=StreamListener, aync=True)
        stream.filter(follow = [str(twitter_id)]) 
        
    except Exception as ex:
        print ("[STREAM] Stream stopped! Reconnecting to twitter stream")
        print (ex)
        stream.filter(follow = [str(twitter_id)])

    except KeyboardInterrupt:
        print('Program Exited Gracefully')
        exit(1)