
from collections import Counter
import re
def tokenize(text):
    """
    Take a string and split it into tokens on word boundaries.

    A token is defined to be one or more alphanumeric characters,
    underscores, or apostrophes.  Remove all other punctuation, whitespace, and
    empty tokens.  Do case-folding to make everything lowercase. This function
    should return a list of the tokens in the input string.
    """
    tokens = re.findall("http:\\/\\/t.co\\/[\w]+|[@#][\w']+|[\w']+|[\p]+", text.lower())
    return [token for token in tokens]

class Tweets:
    def __init__(self, tweets):
        self.tweets=list(tweets)
        
        allterms=[]
        for text in [tweet['text'] for tweet in self.tweets]:
            allterms = allterms+tokenize(text)
        self.terms = set(allterms)
        self.counts = Counter(allterms)
        self.docCount=len(self.tweets)
        
    #getTerms in tweets
    def getTerms(self):
        return self.terms

    #get counts of terms
    def getTermCount(self, term):
        return self.counts[term] if term in self.counts else 0

    #return total number of docs
    def getDocCount(self):
        return self.docCount

                  
