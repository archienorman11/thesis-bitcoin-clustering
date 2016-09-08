import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch
from datetime import datetime

import csv

# import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch([elasticsearch_uri])

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        try:

            # decode json
            dict_data = json.loads(data)

            # pass tweet into TextBlob
            tweet = TextBlob(dict_data["text"])

            # determine if sentiment is positive, negative, or neutral
            if tweet.sentiment.polarity < 0:
                sentiment = "negative"
            elif tweet.sentiment.polarity == 0:
                sentiment = "neutral"
            else:
                sentiment = "positive"

            # fix the timestamp format
            # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            timestamp = datetime.strptime(dict_data["created_at"].replace("+0000 ",""), "%a %b %d %H:%M:%S %Y").isoformat()

            fd = open('output.csv','a')
            fd.write('\n' + sentiment + ', ' + timestamp)
            fd.close()

            # output sentiment
            print(timestamp + ":" + sentiment)

            # # add text and sentiment info to elasticsearch
            # es.index(index="sentiment-demo",
            #          doc_type="tweet",
            #          body={"source": dict_data["source"],
            #                "author": dict_data["user"]["screen_name"],
            #                "location": dict_data["user"]["location"],
            #                "followers": dict_data["user"]["followers_count"],
            #                "timestamp": timestamp,
            #                "message": dict_data["text"],
            #                "polarity": tweet.sentiment.polarity,
            #                "subjectivity": tweet.sentiment.subjectivity,
            #                "sentiment": sentiment})

        except:

            # tweet skipped due to processing error

            print("processing exception")
            # print(data)

        return True

    # on failure
    def on_error(self, status):
        print(status)

def run():

    while True:

        try:

            # create instance of the tweepy tweet stream listener
            listener = TweetStreamListener()

            # set twitter keys/tokens
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            # create instance of the tweepy stream
            stream = Stream(auth, listener)

            # search twitter for the keyword
            stream.filter(track=[keyword])

        except:

            continue

run()
