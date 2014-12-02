#!/usr/bin/env pypy
from funcs import *

nds = {}
with io.open(c.get('twitter','thresholdJS')) as f:
    for line in f:
        line = line.split()
        nds[int(line[0])] = None
        nds[int(line[1])] = None

count = 0
groundTrue = {}
with io.open('../twitterCrawler/nds.list') as f:
    for line in f:
        line = [int(x) for x in line.split()]
        groundTrue[line[0]] = line[1]

Graph = []
with io.open('../twitterCrawler/nd.graph') as f:
    for line in f:
        line = [int(x) for x in line.split()]
        Graph.append(line)

log = io.open('missing3.txt','wb')
for nd in sorted(nds.keys()):
    count += 1
    spammers = {}
    print count,
    for line in Graph:
        if line[0] == nd:
            spammers[line[1]] = None
    print len(spammers),groundTrue[nd]
    if len(spammers)*1.0/groundTrue[nd] < 0.95:
        log.write(str(nd)+"\n")
        log.flush()
log.close()
