#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import sys
import pymongo
import io
import numpy
from funcs import *

conn = pymongo.Connection()
db = conn.twitter
NODES = db.spammers


def get_cluster_infos():
    print "cluster infos"
    out = io.open("cluster_infos.out","wb")
    cluster = getClusters('twitter')
    spammers = []
    AInDeg = []
    AOutDeg = []
    with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter-30000-0.9.clusterSpammers.groundTrue') as f:
        for line in f:
            spammers.append([int(x) for x in line.split()])
    for i in range(len(cluster)):
        print i
        C = cluster[i]
        inDeg = []
        outDeg = []
        for n in spammers[i]:
            tmp = NODES.find_one({"id":n})
            if tmp["protected"]:
                continue
            '''adding degree infomation'''
            try:
                inDeg.append(tmp["followers_count"])
                outDeg.append(tmp["friends_count"])
                AInDeg.append(tmp["followers_count"])
                AOutDeg.append(tmp["friends_count"])
            except:
                print "missing spammer",n
        inDeg = numpy.array(inDeg)
        outDeg = numpy.array(outDeg)
        '''
        Cluster# & avg in-deg & avg out-deg & spammers & volume & nd & name
        '''
        out.write(str(i+1)
        +" & "+"{:.3f}".format(float(inDeg.sum())/len(inDeg))
        +" & "+"{:.3f}".format(float(outDeg.sum())/len(outDeg))
        +" & "+"{:.3f}".format(len(inDeg)/1000000.)
        +" & "+"{:.3f}".format(outDeg.sum()/1000000.)
        +" & "+str(len(C))
        +" & \\\\\n")
        out.flush()

    inDeg = numpy.array(AInDeg)
    outDeg = numpy.array(AOutDeg)
    out.write("Sum/Mean"
    +" & "+"{:.3f}".format(float(inDeg.sum())/len(inDeg))
    +" & "+"{:.3f}".format(float(outDeg.sum())/len(outDeg))
    +" & "+"{:.3f}".format(len(inDeg)/1000000.)
    +" & "+"{:.3f}".format(outDeg.sum()/1000000.)
    +" & "
    +" & \\\\\n")
    out.flush()

get_cluster_infos()
