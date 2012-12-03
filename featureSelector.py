import math
from tweets import Tweets
import sys
import ujson
import os
import operator
import utils

class ChiFeatureSelector:
    def __init__(self, class1, class2):
        # store the sets of tweets making up each bit of the training set
        self.class1 = Tweets(class1)
        self.class2 = Tweets(class2)

    def getScores(self):
        #chi-squared scores
        scores = {}

        # loop over the words in the extraction corpus \todo determine how to include things like retweet count
        for term in self.class1.getTerms():
            # build the chi-squared table
            n11 = float(self.class1.getTermCount(term))
            n10 = float(self.class2.getTermCount(term))
            n01 = float(self.class1.getDocCount() - n11)
            n00 = float(self.class2.getDocCount() - n10)

            # perform the chi-squared calculation and store
            # the score in the dictionary
            total = n11 + n10 + n01 + n00
            top = ((n11 * n00) - (n10 * n01)) ** 2
            bottom = (n11 + n01) * (n11 + n10) * (n10 + n00) * (n01 + n00)
            chi = (total * top) / bottom
            scores[term] = chi
            
        #note for format
        #for (v, k) in scores:
        #    print str(k) + " : " + str(v)
        return scores

if __name__=="__main__":
    cfs=ChiFeatureSelector(utils.read_tweets(sys.argv[1]), utils.read_tweets(sys.argv[2]))
    print 'Features written to features.%d.json'%os.getpid()
    output = open('features.%d.json'%os.getpid(),'w')
    print>>output, ujson.dumps(cfs.getScores())
    print 'Sorted Features written to features.sort.%d.json'%os.getpid()
    output = open('features.sort.%d.json'%os.getpid(),'w')
    print>>output, ujson.dumps( sorted(cfs.getScores().iteritems(), key=operator.itemgetter(1), reverse=True))
