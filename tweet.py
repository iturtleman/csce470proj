from collections import Counter

class tweet:
    def __init__(self, tweets):
        self.tweets=tweets
        allterms=[term for term for term in [tweet['text'] for tweet in tweets]
        self.terms = set(terms)
        self.counts = collections.Counter(allterms)
        self.docCount=len(tweets)
        
    #getTerms in tweets
    def getTerms(self):
        return self.terms

    #get counts of terms
    def getTermCount(self, term):
        return self.counts[term] if term in self.counts else 0

    #return total number of docs
    def getDocCount(self):
        return self.docCount

                  
