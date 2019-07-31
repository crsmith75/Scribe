from datetime import datetime
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer
import os
import pandas as pd
import sys
import time
import tweepy

from twitteraccounts.api.credentials import FCT_ADDRESS, EC_ADDRESS, TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET

#authorizes your twitter api keys
auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET) #Gathers Twitter Keys
auth.set_access_token(TWITTER_APP_KEY, TWITTER_APP_SECRET) #Gathers Twitter APP Keys
api = tweepy.API(auth)

def createChain(tweet_id):

    fct_address = FCT_ADDRESS
    ec_address = EC_ADDRESS

    factomd = Factomd(
    host='http://18.222.184.135:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    walletd = FactomWalletd(
    host='http://18.222.184.135:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    resp = walletd.new_chain(factomd, 
                            [ "TwitterBank Record",str(tweet_id), "testing_web_app10"],
                            "This is the start of this users TwitterBank Records", 
                            ec_address=ec_address) 
                    
    chain_ID = resp['chainid']
    time.sleep(1)

    return chain_ID

def factomizeTweets(tweetid,chain_id):

    private_key, public_key = identitykeys.generate_key_pair() #generates a public, private key pare
    private = private_key.to_string()
    public = public_key.to_string()
    message = b'TwitterBank Record'
    signature = private_key.sign(message)
    sig = signature #base64 encoded pseudo signature

    fct_address = FCT_ADDRESS
    ec_address = EC_ADDRESS

    #initializes factomd --> host will need to be changed to your server address
    factomd = Factomd(
    host='http://18.222.184.135:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    #initializes walletd --> host will need to be changed to your server address
    walletd = FactomWalletd(
    host='http://18.222.184.135:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
    )

    try:
        status = api.get_status(int(tweetid)) #uses a tweet id to recreate an entire status/tweet object 
        userid = status.user.id #gets the user or twitterid for the account
        user_id = str(userid).replace("'", '"') # converts the above string from a single quote string to a double quote string for better JSON representation

        tweetid = str(status.id)
        tweet_id = str(tweetid).replace("'", '"') # converts the above string from a single quote string to a double quote string for better JSON representation

        date = datetime.now()
        date2 = str(date).replace("'", '"')
        fct_entry = {"Date_Recorded": date2,
                    "tweet": status._json}

        print('Sending Tweet to Factom!')

        tweet = fct_entry["tweet"]
            
        try:
            chain_id = str(chain_id)
                
            resp = walletd.new_entry(factomd, chain_id, 
                                    [ 'TwitterBank Chain',user_id, tweet_id, public, sig],
                                    json.dumps(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
                
            entryhash = resp['entryhash']

            time.sleep(10)


        except exceptions.FactomAPIError as e:
            print(e.data)
            print('ERROR')
            return True
            

    except tweepy.TweepError:
        time.sleep(60 * 15)
        print('this messed up')
        #continue
    print('processing next tweet')

"""
The Below Function is used to take a csv of a tracked twitter account's tweets and clean it so that
only the tweets native to the account will be present (i.e no retweets, relplies, etc). It takes a 
csv file of tweets as an input and then uses pandas to clean the tweets and return a new csv of 
clean data.
"""

def filterTweets(file):

    retweet_ids = []

    data = pd.read_csv(file)

    df = pd.DataFrame(data)
    retweets = df[df['text'].str.startswith('RT')]

    for item in retweets['id']:
        retweet_ids.append(item)

    clean_tweets = df[~df['id'].isin(retweet_ids)]

    filename = (file[0:-4] + '_clean' + '.csv') #creates a new file of the form 'orignalname_clean.csv'
    print(filename)


    new_csv = clean_tweets.to_csv(filename, index=False) 

    return new_csv

"""
This is a function used to gather ~3000 of an account's most recent tweets and write them to a csv
file for analysis. It takes a user's twitter handle as an input and then will continue iterating
until all of the tweets are gathered. Unfortunately, due to tweepy api limitations and twitter dev
policy, the maximum number of tweets it can gather for an account is hardcapped at 3240.
"""
def getAllTweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1 #save the id of the oldest tweet less one
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass

"""
Below is a function that takes a csv file as an input as well as a kafka topic (in this case twitter handle).
and then reads the file, isolates on the tweet ids and then writes them to a kafka stream, through a kafka-producer
so that the tweet ids may be consumed by a kafka consumer at a later time.
"""
def sendTweets(file, topic):
        data = pd.read_csv(file) #reads a csv file of tweets
        df = pd.DataFrame(data)

        df_ids = df['id'] #defines a data frame object of only the row in the csv with tweetids

        for tweetid in df_ids:
            try:
                tweet_id = str(tweetid)
                kafka = KafkaClient("localhost:9092") #initializes kafka client
                producer = SimpleProducer(kafka, value_serializer=('utf-8')) #initializes kafka producer
                
                producer.send_messages((str(topic)), tweet_id.encode('utf-8')) #sends tweet ids for the given topic to a message queue      

                time.sleep(2) 

            except tweepy.TweepError: 
                time.sleep(60 * 15)
                print('this messed up')
                continue

