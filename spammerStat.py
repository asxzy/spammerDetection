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
    out = io.open("cluster_infos.out","ab")
#    cluster = getClusters('twitter')
#    spammers = []
#    with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter-30000-0.9.clusterSpammers.groundTrue') as f:
#        for line in f:
#            spammers.append([int(x) for x in line.split()])
#    for i in range(len(cluster)):
#        C = cluster[i]
#        NonSpammers = 0
#        inDeg = []
#        outDeg = []
#        for n in spammers[i]:
#            tmp = NODES.find_one({"id":n})
#            '''adding degree infomation'''
#            try:
#                inDeg.append(tmp["followers_count"])
#                outDeg.append(tmp["friends_count"])
#            except:
#                print "missing spammer",n
#        '''
#        Cluster# & avg in-deg & avg out-deg & spammers & volume & nd & name
#        '''
#        out.write(str(i+1)
#        +" & "+"{:.2f}".format(average(inDeg))
#        +" & "+"{:.2f}".format(average(outDeg))
#        +" & "+"{:,}".format(len(spammers[i]))
#        +" & "+"{:,}".format(numpy.sum(outDeg))
#        +" & "+str(len(C))
#        +" & \\\\\n")
#        out.flush()
    inDeg = []
    outDeg = []
    spammers = []
    with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter-30000-0.9.spammers.groundTrue') as f:
        for line in f:
            spammers.append(int(line))

    for spammer in spammers:
        spammer = NODES.find_one({"id":spammer})
        if spammer == None:
            print spammer
        inDeg.append(spammer["followers_count"])
        outDeg.append(spammer["friends_count"])
    inDeg = numpy.array(inDeg)
    outDeg = numpy.array(outDeg)
    out.write("Sum/Mean"
    +" & "+"{:.2f}".format(float(inDeg.sum())/len(inDeg))
    +" & "+"{:.2f}".format(float(outDeg.sum())/len(outDeg))
    +" & "+"{:,}".format(len(inDeg))
    +" & "+"{:,}".format(outDeg.sum())
    +" & "
    +" & \\\\\n")
    out.flush()
   


get_cluster_infos()
