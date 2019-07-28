from factom import Factomd, FactomWalletd, exceptions #python Factom API
from twitteraccounts.api.credentials import FCT_ADDRESS, EC_ADDRESS
import sys
import time

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