#!/usr/bin/env pypy
from funcs import *

clusters = getClusters('twitter')
C = [{}.fromkeys(x) for x in clusters]
fout = io.open('spammers','wb')
count = 0
for cluster in C:
    count += 1
    print count,cluster
    spammers = {}
    with io.open('../twitterCrawler/nd.graph') as f:
        for line in f:
            line = line.split()
            if int(line[0]) in cluster:
                spammers[int(line[1])] = None
    print len(spammers)
    fout.write("\t".join([str(x) for x in sorted(spammers.keys())]))
    fout.write("\n")
