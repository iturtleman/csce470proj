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
chi_values = {'via' : 1.5, 'twitter' : 1.5, 'the' : 1.5, 'party' : 1.5, 'martes' : 1.5, 
    'join' : 1.5, 'feliz' : 1.5, 'est' : 1.5, '@stacieinatlanta' : 1.5, '2pm' : 1.5,
    '16' : 1.5, '11' : 1.5, '1' : 1.5, '#disneykmart' : 1.5, 'tambi' : 0.6, 'si' : 0.6,
    'rt' : 0.6, 'n' : 0.6, 'muy' : 0.6, 'lqm' : 0.6, 'http://t.co/yeshpffz' : 0.6,
    'http://t.co/mb6lrqh0' : 0.6, 'http://t.co/7xevrait' : 0.6, 'haces' : 0.6,
    'esto' : 0.6, 'en' : 0.6, 'clase' : 0.6, 'bellas' : 0.6, '@silviaarafans' : 0.6,
    '@lapatronatv' : 0.6, '@aracelymridaf' : 0.6, '@aracelyfans_usa' : 0.6,
    '@aracelyfans_mex' : 0.6, '@aracely_fans' : 0.6, '@amada1989' : 0.6}

class TestFeatureSelection(unittest.TestCase):
    def setUp(self):
        self.featureSelector = featureSelector.ChiFeatureSelector(TREND_CORPUS, NONTREND_CORPUS)
        
        
    # add tests here
    def test_feature_selector(self):
        x = self.featureSelector.select('asdf')
        for key,chi in x.items():
            self.assertAlmostEqual(chi, chi_values[key])
        pass

if __name__ == '__main__':
    unittest.main()

