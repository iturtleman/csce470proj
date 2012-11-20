#!/usr/bin/env python

import sys
import tweepy
import os
from tweepy.parsers import JSONParser as Parser
import ujson as json
import fileinput
from settings import settings as s

tweet_ignore = [
    'contributors', 'in_reply_to_screen_name',
    'truncated', 'id_str', 'retweeted_status',
    'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
    'favorited', 'geo', 'user_id_str',
    'possibly_sensitive_editable', 'possibly_sensitive','truncated'
    ]

user_ignore = [
    'contributors_enabled', 'follow_request_sent', 
    'profile_background_color', 'profile_background_image_url',
    'profile_background_image_url_https', 'default_profile_image',
    'profile_background_tile', 'profile_link_color',
    'profile_sidebar_border_color', 'profile_sidebar_fill_color',
    'profile_text_color', 'profile_use_background_image',
    'show_all_inline_media', 'status', 'notifications',
    'id_str', 'is_translator', 'profile_image_url', 'protected',
    'time_zone', 'default_profile', 'listed_count', 'geo_enabled',
    'verified', 'following'
    ]

def strip_dict(d,trash):
    for field in trash:
        if field in d:
            if field == 'retweeted_status':
                d['retweeted_from']=d['retweeted_status']['id_str']
            del d[field]
    nulls = [k for k,v in d.iteritems() if v==None]
    for key in nulls:
        del d[key]

seen = set()

CONSUMER_KEY = s['consumer_key']
CONSUMER_SECRET = s['consumer_secret']
ACCESS_KEY = s['access_key']
ACCESS_SECRET = s['access_secret']
STARTTWEETID = '267803772670066688'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, parser=Parser())

r = api.retweets(STARTTWEETID, 100)

print 'outfile %d.json'%os.getpid()
output = open('tweets.%d.json'%os.getpid(),'w')

for tweet in r:
    if 'user' not in tweet or tweet['id'] in seen:
        continue
    if tweet['user']['followers_count'] > 100:
        print 'followers, id:',tweet['id']
    if tweet['retweeted'] == True:
        print 'retweet id:',tweet['id']
    strip_dict(tweet,tweet_ignore)
    strip_dict(tweet['user'],user_ignore)
    if tweet: # filter out keep-alive new lines
        print>>output, json.dumps(tweet)

print 'done'
