#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pymongo
import io
import numpy
import time
from datetime import datetime
from funcs import *

conn = pymongo.Connection()
db = conn.twitter
NODES = db.spammers


def average(l):
    return reduce(lambda x, y: x + y, l) / float(len(l))

def get_cluster_infos():
    print "cluster infos"
    out = io.open("cluster_infos.out","wb")
    cluster = getClusters('twitter')
    spammers = []
    with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter-30000-0.9.clusterSpammers.groundTrue') as f:
        for line in f:
            spammers.append([int(x) for x in line.split()])
    for i in range(len(cluster)):
        C = cluster[i]
        NonSpammers = 0
        inDeg = []
        outDeg = []
        volume = 0
        for n in spammers[i]:
            tmp = NODES.find_one({"id":n})
            '''adding degree infomation'''
            try:
                inDeg.append(tmp["followers_count"])
                outDeg.append(tmp["friends_count"])
            except:
                print "missing spammer",n
        '''
        Cluster# & avg in-deg & avg out-deg & spammers & volume & nd & name
        '''
        out.write(str(i+1)
        +" & "+"{:.2f}".format(average(inDeg))
        +" & "+"{:.2f}".format(average(outDeg))
        +" & "+"{:.2f}".format(len(spammers[i]))
        +" & "+"{:.2f}".format(numpy.sum(outDeg))
        +" & "+str(len(C))
        +" & "
        +" & \\\\\n")
        out.flush()

get_cluster_infos()
