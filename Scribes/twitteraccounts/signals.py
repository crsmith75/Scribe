from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

import json
from kafka import SimpleProducer, KafkaClient, KafkaConsumer
import pickle

from core.utils import generate_random_string
from django.core import serializers
from twitteraccounts.models import twitterAccount
from twitteraccounts.api.serializers import twitterAccountSerializer

from twitteraccounts.api.asyncfxns import tweetFetcher
from twitteraccounts.api.credentials import TWITTER_KEY, TWITTER_SECRET, TWITTER_APP_KEY, TWITTER_APP_SECRET
from twitteraccounts.api.utils import createChain
from twitteraccounts.api.utils import sendTweets

import os
import time

@receiver(pre_save, sender=twitterAccount)
def add_slug_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.handle)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string

@receiver(pre_save, sender=twitterAccount)
def add_chainid(sender, instance, *args, **kwargs):
    if instance and not instance.chainid:
        chainid = createChain(instance.twitterid)
        instance.chainid = chainid

@receiver(post_save, sender=twitterAccount)
def send_toMem(sender, instance, *args, **kwargs):
    account = serializers.serialize('json', [ instance, ])
    twitteraccount  = account[1:-1]
    time.sleep(600)
    kafka = KafkaClient("localhost:9092")
    producer = SimpleProducer(kafka, value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    print(twitteraccount)
    producer.send_messages('Scribes-faust', json.dumps(twitteraccount).encode('utf-8'))



