#!/usr/bin/env python
import sys
import os
import ujson as json
import fileinput
import ast


COUNTDISPLAYAMMOUNT=100
seen = set()
print 'Outfile tweets.condense.%d.json'%os.getpid()
output = open('tweets.condense.%d.json'%os.getpid(),'w')
def clean_tweets(lines):
    count = 0
    for line in lines:
        if line:
            try:
                #load ujson
                tweet = json.loads(line)
            except:
                try:
                    #attempt to load from string into dict
                    tweet = ast.literal_eval(line)
                except:
                    #hope this is a dict if not something is going to break
                    if isinstance(line,dict):
                        tweet = line
                    else:
                        print 'Unexpected value:',line,'\n continuing'
                        print type(line)
                        continue

            if not 'id' in tweet or tweet['id'] in seen:
                continue
        
            seen.add(tweet['id'])
            
            #keep only ones that have hashtag data
            if 'entities' not in tweet or tweet['entities']['hashtags'] == []:
                continue
            print>>output, json.dumps(tweet)
            count +=1
            if count%COUNTDISPLAYAMMOUNT==0:
                print count

            

if __name__=="__main__":
    clean_tweets(fileinput.input())
