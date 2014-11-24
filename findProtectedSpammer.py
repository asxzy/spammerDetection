#!/usr/bin/env pypy
from funcs import *
import sys
import io
import pymongo

conn = pymongo.Connection()
db = conn.twitter
SPAMMERS = db.spammers

c = ConfigParser.ConfigParser()
c.read('datasets.cfg')
if __name__ == '__main__':
    data = sys.argv[1]
    clusters = getClusters(data)
    protected = {}
    for spammer in SPAMMERS.find({"protected":True}):
        protected[spammer['id']] = None
    print "protected",len(protected)
    nds = {}
    for nd in getNearDuplicates(data):
        nds[nd] = [0,0]
    with io.open('../twitterCrawler/nd.graph') as f:
        count = 0
        for line in f:
            count += 1
            if count % 1000000 == 0:
                print "nd.graph loaded",count
            line = [int(x) for x in line.split()]
            if line[1] in protected:
                nds[line[0]][1] += 1
            else:
                nds[line[0]][0] += 1
    for cluster in clusters:
        count = [0,0]
        for c in cluster:
            count[0] += nds[c][0]
            count[1] += nds[c][1]
        print 1-float(count[0])/float(count[0]+count[1])
