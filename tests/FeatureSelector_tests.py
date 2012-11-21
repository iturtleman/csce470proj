#!/usr/bin/env python
# script to test your pagerank algorithm

import unittest
import featureSelector
import math
import ujson


def read_tweets(filename):
    for line in open(filename):
        if line:
            yield ujson.loads(line)

TREND_CORPUS = read_tweets('trending.json')
NONTREND_CORPUS = read_tweets('nontrending.json')


class TestFeatureSelection(unittest.TestCase):
    def setUp(self):
        self.featureSelector = featureSelector.ChiFeatureSelector(TREND_CORPUS, NONTREND_CORPUS)
        
        
    # add tests here
    def test_feature_selector(self):
        self.featureSelector.getScores()
        pass

if __name__ == '__main__':
    unittest.main()

