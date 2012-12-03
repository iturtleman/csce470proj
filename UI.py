#!/usr/bin/env python
import sys
import os
import ujson
import fileinput
import scrapeTrends
import featureSelector
import ast
import classifier
import utils
from tweets import Tweets
import re
import tweepy

def inputs():
    keyword = raw_input("Enter keyword to test: ")
    return keyword

#def checkFilter(keywords, lines):
#   while keywords in lines:
        
if __name__=="__main__":
    try:
        scrape()
        cfs = ChiFeatureSelector('trending.%d.json'%os.getpid(), 'nontrending.%d.ujson'%os.getpid())     
    except:    
        classify = classifier.HashtagClassifier()
        classify.condProb = utils.read_conf('classifierTrained.json')
        classify.prior = utils.read_conf('classifier_prior.json') 
    while True:
        keyword = re.sub("""[/:*"<>?|\\\s.;'\[\]]+""", '', inputs())
        if not keyword:
            print 'Please enter a valid phrase'
            continue
        try:
            scrapeTrends.search_tweet(keyword)
        except tweepy.TweepError:
            print 'Please enter a valid phrase'
            continue
        except:
             print 'No internet connection present'
        try:
            tweets = utils.read_tweets('tweets/tweets.%(name)s.json'%{'name':keyword})
        except:
            print 'could not classify keyword'
            continue
        #try:
        print classify.classify(Tweets(tweets))
        #except:
        #    print ''        
    

