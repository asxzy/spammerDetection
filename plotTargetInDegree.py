#!/usr/bin/env pypy
import io
import sys
import os
import pymongo
from random import randint,shuffle
from funcs import *

def random_nodes(n = 5000):
    print "random nodes"
    conn = pymongo.Connection("localhost")
    db = conn.twitter
    NODES = db.nodes
    EDGES = db.graph


    count = {}
    '''
    random attributes
    '''
    rand = []
    with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/twitter.randomNodes") as f:
        for line in f:
            rand.append(int(line))


    shuffle(rand)
    rand = rand[:n]

    targets = {}
    for target in EDGES.find({"from":{"$in":rand}}):
        targets[target["to"]] = True
    with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/TargetInDegree/random.tab","wb") as f:
        index = 0
        for target in targets:
            index += 1
            if index % 10000 == 0:
                print index,len(targets)
            f.write(str(EDGES.find({"to":target}).count()))
            f.write("\t")
            count = EDGES.find({"to":target,"spammed":True}).count()
            f.write(str(count))
            f.write("\n")
    print "done"

def plot(i):
    conn = pymongo.Connection("localhost")
    db = conn.twitter
    NODES = db.nodes
    EDGES = db.graph


    zbs = []
    clusters = getClusterSpammers('twitter')
    count = 0
    for cluster in clusters:
        if count == i:
            for zb in cluster:
                zbs.append(zb)
        count += 1
    '''
    zbs attributes
    '''

    count = {}
    targets = {}
    for target in EDGES.find({"from":{"$in":zbs}}):
        targets[target["to"]] = True

    with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/TargetInDegree/"+"%02d"%(i+1)+".tab","wb") as f:
        index = 0
        for target in targets:
            index += 1
            if index % 10000 == 0:
                print index,len(targets)
            f.write(str(EDGES.find({"to":target}).count()))
            f.write("\t")
            count = EDGES.find({"to":target,"spammed":True}).count()
            f.write(str(count))
            f.write("\n")
    print "done"


if __name__ == "__main__":
    random_nodes()
    #for i in range(16):
    #    print i
    #    plot(i)
