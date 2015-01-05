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
    conn = pymongo.Connection()
    DB = conn.sina
    NODES = DB.nodes
    count = {}
    '''
    random attributes
    '''
    rand = [x+1 for x in xrange(1185071)]
    shuffle(rand)
    spammers = []
 
    spammers = {}.fromkeys(spammers)
    for attr in ['gender','created_at','friends_count','followers_count','statuses_count']:
        f = io.open("/Volumes/Data/asxzy/datasets/spammer/weibo/cluster/"+attr+"/random.tab","wb")
        for node in rand[:n]:
            node = NODES.find_one({"random":node})
            if node == None:
                continue
            if attr == 'created_at':
                t = datetime.fromtimestamp(node[attr])
                s = time.strptime('200908','%Y%m')
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
    zbs = []
    clusters = getClusterSpammers('weibo')
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
    spammers = {}.fromkeys(zbs[:n])

    for attr in ['gender','created_at','friends_count','followers_count','statuses_count']:
        f = io.open("/Volumes/Data/asxzy/datasets/spammer/weibo/cluster/"+attr+"/"+"%02d"%(i+1)+".tab","wb")
        with io.open('/Volumes/Data/asxzy/workspace/shared/Weibo/data/node_id-'+attr+'.txt') as fin:
            for line in fin:
                line = line.split()
                if int(line[0]) not in spammers:
                    continue
                if attr == 'created_at':
                    t = time.strptime(line[1],'%Y-%m-%d')
                    t = time.mktime(t)
                    t = datetime.fromtimestamp(t)
                    s = time.strptime('200908','%Y%m')
                    s = time.mktime(s)
                    s = datetime.fromtimestamp(s)
                    line[1] = rrule.rrule(rrule.WEEKLY, dtstart=s, until=t).count()
                elif attr == 'location':
                    if len(line[1]) == 0:
                        line[1] == 'Unknown'
                try:
                    f.write(str(line[1])+'\n')
                except:
                    f.write(str(line[1].encode('utf-8'))+'\n')
            f.close()
        print "Done",i,attr

if __name__ == "__main__":
    random_nodes()
    clusters = getClusters('weibo')
    for i in range(len(clusters)):
        print i
        plot(clusters[i],i)
