#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import pymongo
import io
from random import shuffle
from funcs import *

conn = pymongo.Connection()
db = conn.twitter
NODES = db.nodes
EDGES = db.graph

data = 'twitter'

def S395ByCluster():
    cluster = getClusters(data)
    cmt = []
    for nds in cluster:
        for nd in nds:
            cmt.append(nd)
    matrix = [["Nan" for i in range(len(cmt))] for j in range(len(cmt))]

    with io.open(c.get(data,'nearDuplicatesJS')) as f:
        for line in f:
            line = line.split()
            line[0] = int(line[0])
            line[1] = int(line[1])
            #if float(line[2]) < 0.2:
            #    continue
            i = cmt.index(line[0])
            j = cmt.index(line[1])
            matrix[i][j] = line[2]
            matrix[j][i] = line[2]
    for i in range(len(cmt)):
        matrix[i][i] = "1"


    out = io.open(c.get(data,'thresholdJS')+".ByCluster.matrix","wb")
    for i in matrix:
        out.write("\t".join(i))
        out.write("\n")
    out.close()


def S395():
    cmt = getNearDuplicates(data)
    matrix = [["Nan" for i in range(len(cmt))] for j in range(len(cmt))]

    with io.open(c.get(data,'nearDuplicatesJS')) as f:
        for line in f:
            line = line.split()
            line[0] = int(line[0])
            line[1] = int(line[1])
            #if float(line[2]) < 0.2:
            #    continue
            i = cmt.index(line[0])
            j = cmt.index(line[1])
            matrix[i][j] = line[2]
            matrix[j][i] = line[2]
    for i in range(len(cmt)):
        matrix[i][i] = "1"


    out = io.open(c.get(data,'thresholdJS')+".ByID.matrix","wb")
    for i in matrix:
        out.write("\t".join(i))
        out.write("\n")
    out.close()


def spammers():
    zbs = getSpammers(data)
    print len(zbs)

    N = 1000
    shuffle(zbs)
    zbs = zbs[:N]
    zbs.sort()

    print len(zbs)

    targets = {}
    for zb in zbs:
        targets[zb] = []
        for edge in EDGES.find({"from":zb}):
            targets[zb].append(edge["to"])

    matrix = [["NaN" for i in range(len(zbs))] for j in range(len(zbs))]

    count = 0
    for i in range(len(zbs)):
        for j in range(i,len(zbs)):
            count += 1
            if count % 10000 == 0:
                print count,N*(N-1)/2
            s1 = {}.fromkeys(targets[zbs[i]]).keys()
            s2 = {}.fromkeys(targets[zbs[j]]).keys()
            JS = {}.fromkeys(s1+s2)
            n1 = len(s1)+len(s2)-len(JS)
            js = 0
            try:
                js = n1 / float(len(s1) + len(s2) - n1)
            except:
                js = 0
            if js > 0 and js < 1:
                matrix[i][j] = str(js)
                matrix[j][i] = str(js)
            matrix[i][j] = str(n1)
            matrix[j][i] = str(n1)

    for i in range(len(zbs)):
        matrix[i][i] = "1"


    out = io.open(c.get(data,'spammers')+".ByID.matrix","wb")
    for i in matrix:
        out.write("\t".join(i))
        out.write("\n")
    out.close()

def spammer_cluster():
    zbs = getSpammers(data)
    print len(zbs)

    N = 1000
    shuffle(zbs)
    zbs = zbs[:N]
    zbs.sort()

    print len(zbs)

    targets = {}
    for zb in zbs:
        targets[zb] = []
        for edge in EDGES.find({"from":zb}):
            targets[zb].append(edge["to"])

    zbs = {}.fromkeys(zbs)
    spammer = []
    for cmt in getClusterSpammers(data):
        for s in cmt:
            if s in zbs and s not in spammer:
                spammer.append(s)
    zbs = spammer
    matrix = [["NaN" for i in range(len(zbs))] for j in range(len(zbs))]

    count = 0
    for i in range(len(zbs)):
        for j in range(i,len(zbs)):
            count += 1
            if count % 10000 == 0:
                print count,N*(N-1)/2
            s1 = {}.fromkeys(targets[zbs[i]]).keys()
            s2 = {}.fromkeys(targets[zbs[j]]).keys()
            JS = {}.fromkeys(s1+s2)
            n1 = len(s1)+len(s2)-len(JS)
            js = 0
            try:
                js = n1 / float(len(s1) + len(s2) - n1)
            except:
                js = 0
            if js > 0 and js < 1:
                matrix[i][j] = str(js)
                matrix[j][i] = str(js)
            matrix[i][j] = str(n1)
            matrix[j][i] = str(n1)

    for i in range(len(zbs)):
        matrix[i][i] = "1"


    out = io.open(c.get(data,'spammers')+".ByCluster.matrix","wb")
    for i in matrix:
        out.write("\t".join(i))
        out.write("\n")
    out.close()


if __name__ == "__main__":
    #G81()
    #PDIST()
    S395()
    S395ByCluster()
    #S395_Group()
    #groupTargetUion()
    #t395TargetUion()
    #spammers()
    spammer_cluster()

