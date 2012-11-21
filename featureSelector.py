import math
from tweets import Tweets

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

        # sort the scores in descending order
        scores = sorted([(v, k) for (k, v) in scores.items()], reverse = True)
        i = 0

        #note for format
##        for (v, k) in scores:
##            print str(k) + " : " + str(v)
        return scores