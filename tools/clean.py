#!/usr/bin/env python
import sys
import os
import ujson as json
import fileinput
import ast

# This is a tool I used to shrink the data returned by the streaming api. There
# are a lot of fields it returns that are mostly useless, and removing them
# makes the data about a third the size. It also removes things that are not
# tweets and duplicate tweets. It reads json from stdin and writes json to
# stdout.

tweet_ignore = [
    'contributors', 'in_reply_to_screen_name',
    'truncated', 'id_str', 'retweeted_status',
    'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
    'favorited', 'geo', 'user_id_str',
    'possibly_sensitive_editable', 'possibly_sensitive','truncated',
    
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
    'verified', 'following', 'profile_image_url_https', 'url',
    ]

def strip_dict(d,trash):
    for field in trash:
        if field in d:
            del d[field]
    nulls = [k for k,v in d.iteritems() if v==None]
    for key in nulls:
        del d[key]

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
                    if isinstance(line,str):
                        tweet = line
                    else:
                        continue

            if 'user' not in tweet or not 'id' in tweet or tweet['id'] in seen:
                continue
        
            seen.add(tweet['id'])
            
            #keep only ones that have hashtag data
            if 'entities' not in tweet or tweet['entities']['hashtags'] == []:
                continue
            strip_dict(tweet,tweet_ignore)
            strip_dict(tweet['user'],user_ignore)
            print>>output, json.dumps(tweet)
            count +=1
            if count%10000==0:
                print count

            

if __name__=="__main__":
    clean_tweets(fileinput.input())
