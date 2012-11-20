#!/usr/bin/env python
import os
import tweetstream
import clean
from settings import settings as s

# This reads tweets from Twitter's streaming API and writes them to a file.
# See Twitter's documentation here:
# https://dev.twitter.com/docs/api/1/post/statuses/filter
# You will need to change the SCREEN_NAME and PASSWORD below.
r = tweetstream.SampleStream(s['user'], s['pw'])

count = 0
#output = open('tweets.%d.json'%os.getpid(),'w')

clean.clean_tweets(r)
##for line in r:
##    if line: # filter out keep-alive new lines
##        print>>output, line
##        count +=1
##        if count%100==0:
##            print count

print 'done'
