#!/usr/bin/env pypy
from funcs import *

nds = []
with io.open(c.get('twitter','thresholdJS')) as f:
    for line in f:
        line = line.split()
        nds.append([line[0],line[1]])

spammers = {}
count = 0
groundTrue = {}
with io.open('../twitterCrawler/nds.list') as f:
    for line in f:
        line = [int(x) for x in line.split()]
        groundTrue[line[0]] = line[1]

Graph = []
with io.open('../twitterCrawler/nd.graph') as f:
    for line in f:
        Graph.append(line.split())

log = io.open('missing3.txt','wb')
for nd in nds:
    count += 1
    print count,
    tmp_spammers = {}
    for line in Graph:
        if line[0] == nd[0] or line[0] == nd[1]:
            try:
                tmp_spammers[int(line[1])] += 1
            except:
                tmp_spammers[int(line[1])] = 1
    countSpammers = 0
    for spammer in tmp_spammers:
        if tmp_spammers[spammer] == 2:
            countSpammers += 1
            spammers[spammer] = None
    print groundTrue[int(nd[0])],groundTrue[int(nd[1])],countSpammers,nd
    if countSpammers*1.0/min(groundTrue[int(nd[0])],groundTrue[int(nd[1])]) < 0.9:
        log.write(nd[0]+"\n"+nd[1]+"\n")
        log.flush()
log.close()
sys.exit()
fout = io.open('spammers.txt','wb')
for spammer in sorted(spammers.keys()):
    fout.write(str(spammer)+'\n')
fout.close()

clusters = getClusters('twitter')
C = [{}.fromkeys(x) for x in clusters]

fout = io.open('spammersCluster.txt','wb')

count = 0
for cluster in C:
    count += 1
    print count,cluster
    out = {}
    with io.open('../twitterCrawler/nd.graph') as f:
        for line in f:
            line = line.split()
            if int(line[0]) in cluster and int(line[1]) in spammers:
                out[line[1]] = None
    print len(out)
    fout.write("\t".join([str(x) for x in sorted(out.keys())]))
    fout.write("\n")
fout.close()
