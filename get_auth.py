#!/usr/bin/env python
import tweepy

CONSUMER_KEY = 'key'
CONSUMER_SECRET = 'secret'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

try:
    auth_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'
print auth_url

print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print 'Error! Failed to get access token.'

print 'Access Key: ',auth.access_token.key
print 'Access Secret: ',auth.access_token.secret

