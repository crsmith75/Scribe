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
Explorer (either the TFA Explorer or the Factom Control Panel). A Beta-version of the sftware with this functionality if completed, however, rigorous testing still needs to be completed before the software is production ready. I have included the scripts being used in a separate folder titled "Python Factomization Scripts" so that you can see how the software works, and what is being done behind the scenes or if you wish to contribute to the Repo yourself. For more information on how faust works for this process if you are interested or wish to collaborate on syncing up the asynchronous task and message queues you can find more information here: https://github.com/robinhood/faust

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

Once in your virtual environment run `pip install -r requirements.txt`. This will give you all of the dependencies you need
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
Replace the values for all of these with the ones you just acquired and save. . You will also need to set the address of your testnet server in the createChain and FactomizeTweets methods in the Scribes/Scribes/twitteraccounts/api/utils.py file.


You will also need to install kafka. To do so, go to https://kafka.apache.org/downloads. I found this guide particularly helpful for installing and running kafka on a Mac: https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273. If you are using a windows machine, this guide appeared to be fairly straight forward https://medium.com/@shaaslam/installing-apache-kafka-on-windows-495f6f2fd3c8. Lastly if you are on an Ubuntu system, Digital Ocean has provided thorough documentation on the installation and setup process here: https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-18-04. **Note** Ideally this portion will eventually be dockerized so that only a single docker image will take care of this step, however, since the software is still in development and in early beta, zookeeper and kafka must be installed and started/ran manually on your machine. Once you have started your kafka and zookeeper instances, navigate back to the Scribes directory
where there is a manage.py file run the following commands:
```
python manage.py makemigrations
python manage.py migrate
```

If you run into any errors it could be on account of the squlite3 db that django uses as a default, so either delete the
file for it and try again or plug another database of your choosing into the settings.py file within the /Scribes/Scribes/ directory. Then, from within this folder run, run:

```
Scribes runserver
```

This will initiate the python server, and the Django based backend will be ready to go using a sqlite3 database on your local machine. With the python server now running, open a separate terminal and navigate to the /Scribes/frontend/ directory. Make sure you have the latest version of node installed on your machine and then run `npm run serve`. This will start the development server
for the frontend application and if you navigate to http://127.0.01:8000 in your browser you should be good to go! In a third terminal window navigate to the /Scribes/twitteraccounts/api/ directory and run the following command:

```
faust -A Scribes_faust worker -l info
```
This will start the faust application on the backend so that when you add an account to be tracked through the UI, the backend will automatically begin setting up a streamer, scraping tweets, and writing them to Factom.

**Note**
The exact number of workers/agents still has to be determined for the application. Running the above line will start a single worker, however, if it is necessary to start multiple workers to handle the load/computation, then something like the following may be done:
```
faust -A Scribes_faust worker -l info --web-port 6066
faust -A Scribes_faust worker -l info --web-port 6067
faust -A Scribes_faust worker -l info --web-port 6068
```
Running each line in a separate terminal as pictured above would start three workers for the software to manage the computation that would be listening to the kafka server on ports 6066, 6067, and 6068. The default port for faust is 6066. Again, this step will also need to be dockerized at a later time to simply deployment, but this is how it must be done manually at the current stage of development.

**Note** This multi-server system is still an artifact of the system being in development mode, once this moves to production,
only a single server will need to be run the Vue frontend and django backend, and the kafka and faust deployment can be automated via dockerfiles.

You will be navigated to a Login Screen. If you have already created an account login, otherwise click 'Create An Account' and 
then fill out the corresponding form. Once you do you will enter the home screen which is a simple UI with a form and list
where you can add and manage the accounts you want to track. Simply enter a users twitter handle and twitter id and then a 
chain will be created for the account. To find an account's twitter id, visit https://tweeterid.com/ and enter their twitter
handle and the twitter id will be provided for you. Once you hit submit/enter button in roughly 10 minutes you will see the account appear on the UI with its corresponding chainid on the Factom testnet. Note, the chain is created instantly, however, due to timing issues with the mempool and writing of tweets to the chain, this was the most optimal solution I could devise at the time. Another area of future research will be to create a more accomodating UI or backend solution so that the User Experience is more optimal.
With that, you should be good to go! Feel free to track whichever accounts you would like. Another note, the chain ID is derived from the extids used in the createChain method in the /Scribes/twitteraccounts/api/utils.py file. Change the third entry to whatever suits your desired purpose for running the software. Once in production, something concret will be set, however, as there are still numerous things to be tested, it is likely that the same account will need to be ran multiple times, so you may need to change it to avoid a 'INVALID PARAMS' error from the Factom API for trying to create a chain that already exists.

## Next Steps:

1.) Flesh out Error Handling to account for things like an invalid twitter handle or id.

2.) Allow Scribes to add accounts other Scribes are tracking

3.) Implement some sort of incentive structure to reward those who are tracking more accounts/tweets

4.) Build out Consumer Facing Portion

5.) Integrate with bot to periodically tweet every time tracked accounts have tweeted and it was secured with Factom

6.) Deleted Tweet Detection

7.) Integration with Identities

8.) Ongoing modification/optimization of backend asynch programs
