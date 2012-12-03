#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from collections import Counter
import math
import operator
import heapq
import random
import time
import re
import itertools
import utils
import ujson
import tweets

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

class HashtagClassifier(object):
    def __init__(self):
        self.condProb = {}
        self.prior = {}
        self.lastConfusion = {}
    
    def train_on_filtered(self, filtered_tweets):
        """
        purpose: train a bayesian classifier on labeled tweets.
        parameters:
            filtered_tweets - a dictionary mapping class names to a list of
            tweets in that class
        returns: None
        """
        pos = filtered_tweets['pos']
        neg = filtered_tweets['neg']

        #Vocabulary
        V = set()
        #Number of total documents
        N = pos.docCount+neg.docCount

        for val in filtered_tweets.values():
            V.update(val.terms)
        
        condProb = {}
        #number of items in Vocabulary
        B = len(V)
        
        for c,docs in filtered_tweets.iteritems():
            docCount = docs.docCount
            self.prior[c] = math.log(float(docCount)/N)
            concatText = docs.counts

            denom = sum(concatText.values())+B            
            for doc in docs:
                #text = [tokenize(doc["text"])]
                for token in V:
                    if token in condProb:
                        condProb[token][c] = math.log((concatText[token]+1.)/(denom))
                    else:
                        condProb[token] = {c:math.log((concatText[token]+1.)/(denom))}
        self.condProb=condProb
        
    # You'll need a way to calculate the sentiment of a tweet when this code
    # is used by index.py.
    def classify_filtered(self, tweets):
        #we want to classify each of the tweets
        classified = {}
        all_ids = {}
        all_ids['positive']=[ doc['id'] for doc in tweets['positive']]
        all_ids['negative']=[ doc['id'] for doc in tweets['negative']]
        for c,docs in tweets.iteritems():
            classified[c] = self.classify(docs)
        
        #let's get our confusion matrix
        confusion = {'positive':0, 'negative':0, 'falsepos':0, 'falseneg':0}
        for c,ids in classified.items():
            for id, val in ids.items():
                if c == val:
                    confusion[c]+=1
                elif c == 'positive':
                    confusion['falseneg']+=1
                else:
                    confusion['falsepos']+=1

        #print confuse
##        print '\tPosExp\tNegExp'
##        print 'PosAct\t',confusion['positive'],'\t',confusion['falsepos']
##        print 'NegAct\t',confusion['falseneg'],'\t',confusion['negative']

        #save last run for comparison
        self.lastConfusion = confusion
        #merge the two sets into one and return
        
        return dict(classified['positive'].items()+classified['negative'].items())
        
    #this actually classifies the data and returns it
    def classify(self,tweets):
        retval = {}
        for tweet in tweets:
            retval[tweet['id']] = self.classify_one(tweet)
        return retval

    #to make obtaining data from indexing easier
    def classify_one(self,tweet):
        chancePos=self.prior['positive']
        chanceNeg=self.prior['negative']
        for tok in tokenize(tweet['text']):
            if tok in self.condProb:
                chancePos+=self.condProb[tok]['positive']
                chanceNeg+=self.condProb[tok]['negative']
        return 'positive' if chancePos > chanceNeg else 'negative'
        

# taken from http://en.wikipedia.org/wiki/List_of_emoticons
TRENDING_WORDS = set()
NONTRENDING_WORDS = set()

def approx_Equal(x, y, tolerance=0.001):
    return abs(x-y) <= 0.5 * tolerance * (x + y)

def main():
    filtered = filterFeatures(open('features.159168.json')).keys()
    posTweets = tweets.Tweets(utils.read_tweets('tweets/tweets.Trend.json'))
    negTweets = tweets.Tweets(utils.read_tweets('tweets/tweets.nonTrend.json'))
    
    for term in filtered:
        pospercent = posTweets.counts[term]/posTweets.docCount if term in posTweets.counts else 0
        negpercent = negTweets.counts[term]/posTweets.docCount if term in negTweets.counts else 0
        if approx_Equal(pospercent, negpercent):
            continue
        if pospercent > negpercent:
            TRENDING_WORDS.add(term)
        else:
            NONTRENDING_WORDS.add(term)
    print 'trending dict written to trend_words.json'
    output = open('trend_words.json','w')
    print>>output, ujson.dumps(TRENDING_WORDS)

    print 'trending dict written to nontrend_words.json'
    output = open('nontrend_words.json','w')
    print>>output, ujson.dumps(NONTRENDING_WORDS)
##    print 'trending:\n',TRENDING_WORDS,'\n\n'
##    print 'nontrending:',NONTRENDING_WORDS
    print 'Begin training'
    analyzer = HashtagClassifier()
    analyzer.train_on_filtered({'pos':posTweets, 'neg':negTweets})

    print 'Trained classifier written to classifierTrained.json'
    output = open('classifierTrained.json','w')
    print>>output, ujson.dumps(analyzer.condProb)
    
    confusion = {'positive':0., 'negative':0., 'falsepos':0., 'falseneg':0.}
    iterations = 10
    filtered = filter_classes(tweets)
    termFreq = {}
    print 'starting training'
    for i in range(iterations):
        
        train_group, eval_group = split_train_eval(filtered)
    

        
        analyzer.train_on_filtered(train_group)

        analyzer.classify_filtered(eval_group)
        for key,val in analyzer.lastConfusion.items():
            confusion[key]+=float(val)/iterations
        for key,val in analyzer.condProb.iteritems():
            if key in termFreq:
                termFreq[key]['positive']+=val['positive']
                termFreq[key]['negative']+=val['negative']
            else:
                termFreq[key]=val

    #print confuse
    print 'After %i iterations:'%iterations
    print '\tPosExp\tNegExp'
    print 'PosAct\t',confusion['positive'],'\t',confusion['falsepos']
    print 'NegAct\t',confusion['falseneg'],'\t',confusion['negative']
    posSorted = sorted(termFreq.iteritems(), key = lambda x:x[1]['positive'])
    posSorted.reverse()
    negSorted = sorted(termFreq.iteritems(), key = lambda x:x[1]['negative'])
    negSorted.reverse()
    print 'Positive correlation words: '
    for val in posSorted[:25]:
        print val[0],val[1]['positive']
    print '\nNegative correlation words: '
    for val in negSorted[:25]:
        print val[0],val[1]['negative']

if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with sentiment after %.3f seconds'%(end_time-start_time)
