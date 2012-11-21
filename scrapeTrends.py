#!/usr/bin/env python

import sys
import tweepy
import os
from tweepy.parsers import JSONParser as Parser
import ujson as json
import fileinput
import time
from settings import settings as s

tweet_ignore = [
    'contributors', 'in_reply_to_screen_name',
    'truncated', 'id_str', 'retweeted_status',
    'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
    'geo', 'user_id_str',
    'possibly_sensitive_editable', 'possibly_sensitive',
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
    'verified', 'profile_image_url_https', 'url', 
    ]

#cleans up data
def strip_dict(d,trash):
    for field in trash:
        if field in d:
            if field == 'retweeted_status':
                d['retweeted_status_id']=d['retweeted_status']['id_str']
            del d[field]
    nulls = [k for k,v in d.iteritems() if v==None]
    for key in nulls:
        del d[key]

#tweets seen
seen = set()

#keys
CONSUMER_KEY = s['consumer_key']
CONSUMER_SECRET = s['consumer_secret']
ACCESS_KEY = s['access_key']
ACCESS_SECRET = s['access_secret']
#set up auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, parser=Parser())


#name for nontrending source user
NonTrendingName = 'nontrending'

#scrapes trending and nontrending data
def scrape():
    CountTimeline=0
    CountTimelineTime=time.time()
    print 'Started at ',time.localtime(CountTimelineTime)
    #get nontrending tags
    tweets = []
    statuses_count = api.get_user(NonTrendingName)['statuses_count']
    #get max_id to get ones before it
    while len(tweets) < statuses_count:
        if(CountTimeline>15):
            time.sleep(time.time()-CountTimelineTime)
        try:
            maxid = max([id for id in [tweet['id'] for tweet in tweets]])
            r=api.user_timeline(NonTrendingName, count = '200', trim_user ='true', max_id = maxid)
        except:
            r=api.user_timeline(NonTrendingName, count = '200', trim_user ='true')
        CountTimeline+=1
        tweets = tweets+r
        
    #output tweets
    print 'nontrending.%d.json'%os.getpid()
    output = open('nontrending.%d.json'%os.getpid(),'w')
    tags = set()
    for tweet in tweets:
        if tweet['id'] in seen:
            continue
        strip_dict(tweet,tweet_ignore)
        tags.update([tag for tag in tweet['text'].split()])
        print>>output, json.dumps(tweet)
    print 'nontrending.%d.tags.json'%os.getpid()
    output = open('nontrending.%d.tags.json'%os.getpid(),'w')
    print>>output, json.dumps(list(tags))
    tags = set()

    
    r=api.trends_weekly()
    for trends in [day for day in r['trends'].values()]:
        tags.update([trend['query'] for trend in trends])

    r=api.trends_daily()
    for trends in [hour for hour in r['trends'].values()]:
        tags.update([trend['query'] for trend in trends])

    print 'trending.%d.tags.json'%os.getpid()
    output = open('trending.%d.tags.json'%os.getpid(),'w')
    print>>output, json.dumps(list(tags))

    print 'done'

#searches for a given tag and returns tweets
def search_tweet(tag,name=""):
    print tag
    if '/' in tag or '?' in tag:
        return
    r = api.search(tag, result_type='mixed', count=100, include_entities='true')
    filename= 'tweets.%(name)s.%(id)d.json'%{'id':os.getpid(),'name':name}
    output = open('tweets/%s'%filename,'a+')

    for tweet in r['results']:
        if tweet['id'] in seen:
            continue
        seen.add(tweet['id'])
        strip_dict(tweet,tweet_ignore)
        if 'user' in tweet:
            strip_dict(tweet['user'],user_ignore)
        print>>output, json.dumps(tweet)
        
def main():
    scrape()

    f = open('nontrending.%d.tags.json'%os.getpid(),'r')
        
    nonTrendTags = json.loads(f.read())
    print 'Getting NonTrending tweets'
    for tag in nonTrendTags:
        search_tweet(tag,'NonTrend')
        
    print 'Getting Trending tweets'
    f=open('trending.%d.tags.json'%os.getpid(),'r')
    trendtags = json.loads(f.read())

    for tag in trendtags:
        search_tweet(tag,'Trend')


if __name__=="__main__":
    main()
