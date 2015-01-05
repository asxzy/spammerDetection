#!/usr/bin/env python
from funcs import *
import io
import sys
import os
import pymongo
from datetime import datetime
from dateutil import rrule
import time
from random import randint,shuffle


def random_nodes(n = 50000):
    conn = pymongo.Connection("localhost")
    db = conn.twitter
    NODES = db.nodes
    EDGES = db.edges

    count = {}
    '''
    random attributes
    '''
    rand = []
    with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/twitter.randomNodes") as f:
        for line in f:
            rand.append(int(line))

    shuffle(rand)
    spammers = []
    for node_id in rand[:n]:
        node = NODES.find_one({"id":node_id})
        if node == None:
            print "missing",node_id
            continue
        spammers.append(node)

 
    #for attr in ['lang','created_at','friends_count','followers_count','statuses_count']:
    for attr in ['protected']:
        f = io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/"+attr+"/random.tab","wb")
        infos = []
        for node in spammers:
            if attr == 'created_at':
                t = time.strptime(node['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                t = time.mktime(t)
                t = datetime.fromtimestamp(t)
                s = time.strptime('200607','%Y%m')
                s = time.mktime(s)
                s = datetime.fromtimestamp(s)
                node['created_at'] = rrule.rrule(rrule.WEEKLY, dtstart=s, until=t).count()

            elif attr == 'location':
                if len(node[attr]) == 0:
                    node[attr] == 'Unknown'
            try:
                f.write(str(node[attr])+'\n')
            except:
                f.write(str(node[attr].encode('utf-8'))+'\n')
        f.close()
        print "Done",attr



def plot(cluster,i,n=50000):
    conn = pymongo.Connection("localhost")
    db = conn.twitter
    NODES = db.spammers
    EDGES = db.edges

    zbs = []
    clusters = getClusterSpammersGroundTrue('twitter')
    count = 0
    for cluster in clusters:
        if count == i:
            for zb in cluster:
                zbs.append(zb)
        count += 1

    shuffle(zbs)
    '''
    zbs attributes
    '''
    spammers = []
    for node_id in zbs[:n]:
        node = NODES.find_one({"id":node_id})
        if node == None:
            print "missing",node_id
            continue
        spammers.append(node)

    #for attr in ['lang','created_at','friends_count','followers_count','statuses_count']:
    for attr in ['protected']:
        f = io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/"+attr+"/"+"%02d"%(i+1)+".tab","wb")
        infos = []
        for node in spammers:
            if attr == 'created_at':
                t = time.strptime(node['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                t = time.mktime(t)
                t = datetime.fromtimestamp(t)
                s = time.strptime('200607','%Y%m')
                s = time.mktime(s)
                s = datetime.fromtimestamp(s)
                node['created_at'] = rrule.rrule(rrule.WEEKLY, dtstart=s, until=t).count()
            elif attr == 'location':
                if len(node[attr]) == 0:
                    node[attr] == 'Unknown'
            try:
                f.write(str(node[attr])+'\n')
            except:
                f.write(str(node[attr].encode('utf-8'))+'\n')
        print "Done",i,attr

if __name__ == "__main__":
    random_nodes()
    clusters = getClusters('twitter')
    for i in range(len(clusters)):
        print i
        plot(clusters[i],i)
