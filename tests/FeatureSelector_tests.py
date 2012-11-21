#!/usr/bin/env python
# script to test your pagerank algorithm

import unittest
import featureSelector
import math

def read_tweets(filename):
    for line in open(filename):
        yield ujson.loads(line)

TREND_CORPUS = read_tweets('trending.json')
NONTREND_CORPUS = read_tweets('nontrending.json')


class TestFeatureSelection(unittest.TestCase):
    def setUp(self):
        self.featureSelector = featureSelector.ChiFeatureSelector(TREND_CORPUS, NONTREND_CORPUS)
        pass
        
        
    # add tests here
    def test_feature_selector(self):
        pass

if __name__ == '__main__':
    unittest.main()

