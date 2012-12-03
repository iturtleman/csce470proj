import ujson

def read_tweets(filename):
    for line in open(filename):
        if line:
            yield ujson.loads(line)
            
def read_conf(filename):
    for line in open(filename):
        if line:
            return ujson.loads(line)
