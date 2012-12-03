#!/usr/bin/env python
import sys
import os
import ujson
import fileinput
import scrapeTrends
import featureSelector
import ast
import classifier


checkWord = {}


def inputs():
    keyword = raw_input("Enter keyword to test: ")
    print keyword

def filterFeatures(lines):
    avg=0.0
    count=0
    vals = {}
    for line in lines:
        vals = ujson.loads(line)
        for key,val in vals.iteritems():
            avg += val
            count +=1
    avg = avg/count
    for key,val in vals.items():
        if val < avg:
            del vals[key]
    return vals

def checkFilter(keywords, lines):
   while keywords in lines:
        
if __name__=="__main__":
    try:
        scrape()
        cfs = ChiFeatureSelector('trending.%d.json'%os.getpid(), 'nontrending.%d.ujson'%os.getpid())     
    except:    
        classifier = HashtagClassifier()
        classfier.condProb = read_tweets('classifierTrained.ujson') 
    keyword = inputs()
    vals = filterFeatures(fileinput.input())
    

