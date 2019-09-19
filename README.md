# Scribe

Consensus Networks in Conjunction with TFA are excited to bring you Scribe. This will be a two sided platform in which there
is one application that will be used by those who want to contribute compute power and factoids to track various account's 
tweets and write them to the Factom Blockchain and then a consumer facing application that can then be used to verify if
a tweet for an account has been secured by factom and if so by how many different accounts. This repository contains the codebasefor the non-consumer facing application, or in other words the software that will be run by those who are securing tweets to the Factom blockchain (Scribes).

## Current Status of the Software:
Scribes can download the software to run as a native webapp, create an account, and have a simple UI interface where they
Can add accounts by entering a twitter handle and twitter id for a factom account. A list of tracked accounts will then 
be populated along with the corresponding Factom Testnet Chain ID for the Chain that will be created of all of that account's
Factomized Tweets. Currently, python scripts are written for the project that will run asynchronously in the background via Robinhood Faust (library and info here: https://github.com/robinhood/faust).

1.) Use an accounts twitter handle to gather the account's ~3000 most recent tweets, clean them so that only the account's
original tweets remain (i.e no retweets) and then write them to a kafka-based message queue that can then be pulled from by 
a kafka consumer and written to the Factom blockchain.

2.) Create a Stream listener that will use the account's twitter id to listen for every time they tweet. It will filter all
retweets, comments, replies, etc. so that only the account's native tweets trigger a response. Then, similarly above, the
tweets will then be written to a message queue in kafka, where they may then be consumed by a kafak-consumer and written 
to the Factom blockchain.

**Disclaimer** Software is still in beta. I have included the python scripts being used in a separate folder titled "Python Factomization Scripts" if you wish to contribute to the Repo yourself or are interested in messing around with them. For more information on how faust works for this process here: https://github.com/robinhood/faust

## Setting Up/Configuring the Software:

If you wish to run the software there are a few prerequisites you will need. First, you will need to get Twitter API Keys and
A Factom Wallet Address. To get Twitter API Keys you will need to go to https://developer.twitter.com/, create a developer
account and then create an app. This will give you four keys you need: Twitter Key, Twitter Secret, Twitter App Key, Twitter App Secret. To get a factom wallet and corresponding FCT and EC Addresses please see the documentation here: https://docs.factom.com/wallet#introduction

Once you have these items you now have everything you need to run the software. Now you must clone the repo. Create a directory that you want to house the project in and then run

`git clone https://github.com/crsmith75/Scribe.git`

Now start your virtual environment and install dependencies:
```
pip install pipenv
pipenv shell
pip install -r requirements.txt
```
Now you need to add your credentials in the credentials.py file. This can
be found within the /Scribes/web/twitteraccounts/api directory of the project. Once you open the file you will see the following:
```
TWITTER_KEY = "YourTwitterKey"
TWITTER_SECRET = "YourTwitterSecret"
TWITTER_APP_KEY = "YourTwitterApp Key"
TWITTER_APP_SECRET = "YourTwitterAppSecret"

#specify RPC credentials:
FCT_ADDRESS = 'YourFCTAddress'
EC_ADDRESS = 'YourECAddress'
```
Replace the values for all of these with the ones you just acquired and save. . You will also need to set the address of your testnet server in the createChain and FactomizeTweets methods in the Scribes/web/twitteraccounts/api/utils.py file.

## Starting Kafka
From the terminal navigate to kafka directory of the project:
```
cd Scribes/kafka/
docker-compose -f kafka-dev.yaml up
```
This will start a zookeeper/kafka cluster with a port exposed at 9092 on localhost.

## Starting Web App
From a new terminal navigate to the web directory:
where there is a manage.py file run the following commands:
```
cd Scribes/web/
python setup.py develop
Scribes runserver
```
This will start a python web server containing the web app with port 8000 exposed on localhost.

## Starting Faust Agent
From a new terminal navigate to the web directory:
```
cd Scribes/web/twitteraccounts/api/
faust -A Scribes_faust worker -l info
```
## Using the Software
You will be navigated to a Login Screen. Click 'Create An Account' and then fill out the corresponding form. Once you do you will enter the home screen which is a simple UI with a form and list where you can add and manage the accounts you want to track. Simply enter a users twitter handle and twitter id and then a chain will be created for the account. 

To find an account's twitter id, visit https://tweeterid.com/ and enter their twitter handle and the twitter id will be provided for you. Once you hit submit/enter button in roughly **10 minutes** you will see the account appear on the UI with its corresponding chainid on the Factom testnet. 

**Note:** The chain is created instantly, however, due to timing issues with the mempool and writing of tweets to the chain, this was the most optimal solution I could devise at the time. 

**Note:** The chain ID is derived from the extids used in the createChain method in the /Scribes/web/twitteraccounts/api/utils.py file. If you get an 'INVALID PARAMS' error from the Factom API when tracking an Account it is because the chain  already exists. Change the third entry to whatever suits your desired purpose for running the software. Once in production, something concrete will be set.

**Note:** If you run into any errors it could be on account of the squlite3 db that django uses as a default, so either delete the file for it and try again or plug another database of your choosing into the settings.py file within the /Scribes/web/Scribes/ directory. 

## Next Steps:

1.) Flesh out Error Handling to account for things like an invalid twitter handle or id.

2.) Allow Scribes to add accounts other Scribes are tracking

3.) Implement some sort of incentive structure to reward those who are tracking more accounts/tweets

4.) Build out Consumer Facing Portion

5.) Integrate with bot to periodically tweet every time tracked accounts have tweeted and it was secured with Factom

6.) Deleted Tweet Detection

7.) Integration with Identities

8.) Ongoing modification/optimization of backend asynch programs
