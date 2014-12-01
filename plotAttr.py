#!/usr/bin/env pypy
from funcs import *
import io
import sys
import os
import pymongo
from datetime import datetime
import time
from random import randint,shuffle


def random_nodes(n = 20000):
    conn = pymongo.Connection("localhost")
    db = conn.twitter
    NODES = db.nodes
    EDGES = db.edges

    count = {}
    '''
    random attributes
    '''
    infos = []
    rand = []
    with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/twitter.randomNodes") as f:
        for line in f:
            rand.append(int(line))

    for attr in ['created_at','friends_count','followers_count','statuses_count']:
        for node_id in rand:
            node = NODES.find_one({"id":node_id})
            if node == None:
                print node_id
                sys.exit()
        #for node in NODES.find({"id":{"$in":rand[:n]}}):
            if attr == 'created_at':
                t = time.strptime(node['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                t = time.mktime(t)
                node['created_at'] = datetime.fromtimestamp(t).strftime("%Y-%m")
            elif attr == 'location':
                if len(node[attr]) == 0:
                    node[attr] == 'Unknown'
            infos.append(node[attr])
        print "len infos",len(infos)
        infos.sort()

        sortedKey = sorted(set(infos))

        for info in infos:
            try:
                count[info]
            except:
                count[info] = 0
            count[info] += 1

        with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/"+attr+"/random.tab","wb") as f:
            index = 0
            for key in sortedKey:
                index += 1
                f.write(str(index))
                f.write("\t")
                f.write(unicode(key))
                f.write("\t")
                try:
                    f.write(str(count[key]*1.0/len(infos)))
                except:
                    f.write("0")
                f.write("\n")
        print "Done",attr



def plot(cluster,i,n=20000):
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
    print len(zbs)
    '''
    zbs attributes
    '''
    for attr in ['created_at','friends_count','followers_count','statuses_count']:
        infos = []
        for node_id in zbs[:n]:
            node = NODES.find_one({"id":node_id})
            if node == None:
                print "missing",node_id
                continue
            if attr == 'created_at':
                t = time.strptime(node['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                t = time.mktime(t)
                node['created_at'] = datetime.fromtimestamp(t).strftime("%Y-%m")
            elif attr == 'location':
                if len(node[attr]) == 0:
                    node[attr] == 'Unknown'
            infos.append(node[attr])
        print "len infos",len(infos)
        infos.sort()

        sortedKey = sorted(set(infos))

        count = {}
        for info in infos:
            try:
                count[info]
            except:
                count[info] = 0
            count[info] += 1
        with io.open("/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/"+attr+"/"+"%02d"%(i+1)+".tab","wb") as f:
            index = 0
            for key in sortedKey:
                index += 1
                f.write(str(index))
                f.write("\t")
                #f.write(str(key.encode("utf-8")))
                f.write(str(key))
                f.write("\t")
                try:
                    f.write(str(count[key]*1.0/len(infos)))
                except:
                    f.write("0")
                f.write("\n")
        print "Done",i,attr

if __name__ == "__main__":
    random_nodes()
    clusters = getClusters('twitter')
    for i in range(len(clusters)):
        print i
        plot(clusters[i],i)
