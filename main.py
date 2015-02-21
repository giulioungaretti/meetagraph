#!/usr/bin/env python
from connect import connect
from tweepy import Cursor
from pycyper import NeoGraph

# connect to twitter api
api = connect()
# fetch a cursro for cph +/- 50 km
c = Cursor(api.search, q='*', geocode="55,13,50km")
# empty containers
tweets = []
ids = []
hashs = []
names = []
# coonnect graph db
graph = NeoGraph(api)
# iterate through items
# TDDO: fetch more
for tweet in c.items():
    tweets.append(tweet)
    ids.append(tweet.user.id)
    hashs.append(tweet.entities.get("hashtags"))
    name = tweet.user.screen_name
    graph.insert_user_with_friends(name)
