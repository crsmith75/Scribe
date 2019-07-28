# Scribe

Consensus Networks in Conjunction with TFA are excited to bring you the first installment of our opensource software for the
Factom-Twitter Project (Current Working Names are "Codex or Vinyl"). This will be a two sided platform in which there
is one application that will be used by those who want to contribute compute power and factoids to track various account's 
tweets and write them to the Factom Blockchain and then a consumer facing application that can then be used to verify if
a tweet for an account has been secured by factom and if so by how many different accounts. This repository contains the codebase
for the non-consumer facing application, or in other words the software that will be run by those who are securing tweets to
the Factom blockchain (Current working name for these Participants is Scribes).

## Current Status of the Software:
Scribes can download the software to run as a native webapp, create an account, and have a simple UI interface where they
Can add accounts by entering a twitter handle and twitter id for a factom account. A list of tracked accounts will then 
be populated along with the corresponding Factom Testnet Chain ID for the Chain that will be created of all of that account's
Factomized Tweets. Currently, python scripts are written for the project that will:

1.) Use an accounts twitter handle to gather the account's ~3000 most recent tweets, clean them so that only the account's
original tweets remain (i.e no retweets) and then write them to a kafka-based message queue that can then be pulled from by 
a kafka consumer and written to the Factom blockchain.

2.) Create a Stream listener that will use the account's twitter id to listen for every time they tweet. It will filter all
retweets, comments, replies, etc. so that only the account's native tweets trigger a response. Then, similarly above, the
tweets will then be written to a message queue in kafka, where they may then be consumed by a kafak-consumer and written 
to the Factom blockchain.

However, the integration of these scripts into the backend as asynchronous tasks is an ongoing effort and is currently underway
using the Robinhood Faust framework to handle asynchronous task management and message queuing so that everytime an account
is added by a Scribe these processes will commense in the background and factomized tweets will be viewable on a Factom Block 
Explorer (either the TFA Explorer or the Factom Control Panel). I have included the scripts being used in a separate folder
titled "Python Factomization Scripts" so that you can see how the software works, and what is being done or if you wish
to contribute to the Repo and contribute to the code base yourself. For more information on how faust works for this process if
you are interested or want to collaborate on syncing up the asynchronous task and message queues you can find more information
here: https://github.com/robinhood/faust

## Running the Software:

If you wish to run the software there are a few prerequisites you will need. First, you will need to get Twitter API Keys and
A Factom Wallet Address. To get Twitter API Keys you will need to go to https://developer.twitter.com/, create a developer
account and then create an app. This will give you four keys you need: Twitter Key, Twitter Secret, Twitter App Key, Twitter App
Secret. To get a factom wallet and corresponding FCT and EC Addresses please see the documentation here: https://docs.factom.com/wallet#introduction

Once you have these items you now have everything you need to run the software. Now you must clone the repo. Create a directory
that you want to house the project in and then run

`git clone https://github.com/crsmith75/Scribe.git`

This will give you the the entire contents of this repository. You will likely want to run this in a virtual environment. I 
personally prefer pipenv, but venv also works just fine. Since the code for the backend is pythonic it just needs to be a 
python based virtual environment. For example, using pipenv run:
`pip install pipenv` followed by `pipenv shell`.

Once in your virtual environment run `pip install requirements.txt`. This will give you all of the dependencies you need
on the python end of things to run the software. Now you need to add your credentials in the credentials.py file. This can
be found within the /Scribes/twitteraccounts/api directory of the project. Once you open the file you will see the following:
```
TWITTER_KEY = "Your Twitter Key"
TWITTER_SECRET = "Your Twitter Secret"
TWITTER_APP_KEY = "Your Twitter App Key"
TWITTER_APP_SECRET = "Your Twitter App Secret"

#specify RPC credentials:
FCT_ADDRESS = 'Your FCT Address'
EC_ADDRESS = 'Your EC Address'
```
Replace the values for all of these with the ones you just acquired and save. Then navigate back to the Scribes directory
where there is a manage.py file. Once in here run the following commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

If you run into any errors it could be on account of the squlite3 db that django uses as a default, so either delete the
file for it and try again or plug another database of your choosing into the settings.py file within the /Scribes/Scribes/ directory.

With the python server now running, open a separate terminal and navigate to the /Scribes/frontend directory. Make sure you have
the latest version of node installed on your machine and then run `npm run serve`. This will start the development server
for the frontend application and if you navigate to http://127.0.01:8000 in your browser you should be good to go!

**Note** This two server system is still an artifact of the system being in development mode, once this moves to production,
only a single server will need to be run

