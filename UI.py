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

checkWord = {}


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
        classify.condProb = utils.read_tweets('classifierTrained.ujson') 
    while True:
        keyword = inputs()
        try:
            scrapeTrends.search_tweet(keyword, keyword)
        except:
             print 'No internet connection present'
        try:
            tweets = utils.read_tweets('tweets/tweets.%(name)s.%(id)d.json'%{'id':os.getpid(),'name':keyword})
        except:
            print 'could not classify keyword'
            continue
        #try:
        classify.classify(tweets)
        #except:
        #    print ''        
    

