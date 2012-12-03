import ujson

def read_tweets(filename):
    for line in open(filename):
        if line:
            yield ujson.loads(line)
