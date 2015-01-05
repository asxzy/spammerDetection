#!/usr/bin/env pypy
from funcs import *
import pymongo

conn = pymongo.Connection()
DB = conn.twitter
NODES = DB.spammers



Icount = 0
Acount = 0
targets = {}
spammers = {}.fromkeys(getClusterSpammersGroundTrue('twitter')[3])
InLinks = 0
for spammer in spammers:
    try:
        InLinks += NODES.find_one({"id":spammer})["followers_count"]
    except:
        print "missing spammer", spammers


with io.open('spammerCluster4.graph') as f:
    for line in f:
        Acount += 1
        line = [int(x) for x in line.split()]
        #spammers[line[0]] = None
        targets[line[1]] = None


with io.open('spammerCluster4.graph') as f:
    for line in f:
        line = [int(x) for x in line.split()]
        if line[1] in spammers:
            Icount += 1

with io.open('spammerCluster4-targets.txt','wb') as f:
    for t in sorted(targets.keys()):
        f.write(str(t)+'\n')

print 'len of spammers',len(spammers)
print 'len of targets',len(targets)
print 'innerloop/AllLinks',Icount,Acount,float(Icount)/Acount
print 'spammer total inlinks',InLinks
