# Scribe
TwitterScribe Software

This is a web application designed for scribes to run for the TwitterFCT project we are doing in conjunction with the TFA. This web application has a pythonic backend comprised of Django rest framework and will have a Vue.js frontend. 

## Prerequisites:

There Are some prerequisites necessary to interact with this software package. Firstly, you must sign up for a twitter developer account and create an app. You may then aquire the following four items:

1.) Twitter Key

2.) Twitter Secret

3.) Twitter API Key

4.) Twitter API Secret

Without these four keys, you will be unable to interact with thte twitter api in any capacity and hence be unable to record/stream/scrape tweets.

Additionally, you must have a Factom Wallet, or some crypto wallet capable of holding Factom. Seeing as Entry Credits or EC is required to submit transactions to Factom, you will need to have an ample supply of entry credits, an FCT address, and an EC address so that you will be able to "Factomize" the tweets after gathering them via the Twitter API.

## How it Works:

The purpose of this software is for those who wish to validate tweets from an account by recording them to the Factom Blockchain. The software works as follows:

1.) Somone choosing to run the software (Scribe is the current working name) downloads the software and creates an account
2.) Scribe adds his/her credentials(FCT Address, EC Address, Twitter Developer Credentials)
3.) Once credentials are loaded, the scribe can add accounts to track by inputing a twitter handle and twitter id for an account
4.) 
  
  a.) Once the account is added, a chain for the account is created on Factom, and the corresponding chain id is returned

  b.) Once the chain is created, two python scripts are initiated. One will begin scraping the account's timeline for up to         ~3000 of the accounts most recent tweets, being sure to filter out retweets & replies, leaving only origninal tweets           from the account. It also will initiate a stream listener using the twitter api and tweepy libraries to stream tweets         from the account. the tweet ids (numeric identifier for the individual tweet) are then published into a message queue         using kafka  The message queue is named, or the topic it is tracking is named after the twitter handle for the account         being trackedAll of this is done using the Faust Library open sourced by Robinhood engineering and both of these scripts       are executed asynchronously in the background.
  
  c.) A faust agent will then consume a tweet id from the message queue for the particular topic, reconstruct the tweet, and 
      write it to Factom using the python api for Factom. The agent will then check the queue every 10 seconds to see if there       is an available message to consume and then it will repeat the process. The agent will wait and subscribe to the topic         as long as the scribe wishes to track the account.
      
 5.) The Scribe may track as many or as few accounts for as long or short as he or she wants. Accordingly the above process will be run for every account the scribe tracks until they decide to cease doing so.
