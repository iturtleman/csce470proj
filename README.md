csce470proj
===========

This project needs you to install 
tweepy
tweetstream
ujson

To run tests, simply run 'nosetests' in the root directory. 

In order to run the code, you must obtain from twitter a consumer key and secret and enter that data into settings.py or settings_local.py.
Then follow the instructions to obtain the Access key and secret which you must also place in the settings files. 

To obtain tweets for end result comparison, simply enter your twitter username and password into the settings file and then run crawl.py.

To obtain tweets for the learning set run scrapeTrends.py

To obtain retweets of a given tweet run 'crawl.py tweetid'